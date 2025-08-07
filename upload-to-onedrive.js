const fs = require('fs').promises;
const path = require('path');
const axios = require('axios');
const yaml = require('js-yaml');
const { glob } = require('glob');

class OneDriveUploader {
  constructor(clientId, clientSecret, refreshToken) {
    this.clientId = clientId;
    this.clientSecret = clientSecret;
    this.refreshToken = refreshToken;
    this.accessToken = null;
  }

  async authenticate() {
    try {
      const response = await axios.post('https://login.microsoftonline.com/consumers/oauth2/v2.0/token', 
        new URLSearchParams({
          client_id: this.clientId,
          client_secret: this.clientSecret,
          refresh_token: this.refreshToken,
          grant_type: 'refresh_token',
          scope: 'https://graph.microsoft.com/Files.ReadWrite'
        }), {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        }
      );

      this.accessToken = response.data.access_token;
      console.log('✅ Successfully authenticated with Microsoft Graph API');
      
      // Update refresh token if a new one is provided
      if (response.data.refresh_token) {
        this.refreshToken = response.data.refresh_token;
        console.log('🔄 Refresh token updated');
      }
      
      return this.accessToken;
    } catch (error) {
      console.error('❌ Authentication failed:', error.response?.data || error.message);
      throw error;
    }
  }

  async uploadFile(filePath, folderId, fileName) {
    if (!this.accessToken) {
      await this.authenticate();
    }

    try {
      const fileContent = await fs.readFile(filePath);
      
      // Check if file exists first (optional - for better logging)
      let fileExists = false;
      try {
        const checkUrl = `https://graph.microsoft.com/v1.0/me/drive/items/${folderId}:/${fileName}`;
        await axios.get(checkUrl, {
          headers: { 'Authorization': `Bearer ${this.accessToken}` }
        });
        fileExists = true;
      } catch (error) {
        // File doesn't exist (404) or other error - we'll create it
        fileExists = false;
      }
      
      // Upload the file (creates new or replaces existing)
      const uploadUrl = `https://graph.microsoft.com/v1.0/me/drive/items/${folderId}:/${fileName}:/content`;
      
      const response = await axios.put(uploadUrl, fileContent, {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'text/markdown'
        }
      });

      const action = fileExists ? 'Updated' : 'Created';
      console.log(`✅ ${action}: ${fileName} in folder ${folderId}`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 401) {
        // Token expired, try to re-authenticate
        console.log('🔄 Access token expired, re-authenticating...');
        await this.authenticate();
        return this.uploadFile(filePath, folderId, fileName);
      }
      
      console.error(`❌ Failed to upload ${fileName}:`, error.response?.data || error.message);
      throw error;
    }
  }

  async createFolder(parentFolderId, folderName) {
    if (!this.accessToken) {
      await this.authenticate();
    }

    try {
      const response = await axios.post(
        `https://graph.microsoft.com/v1.0/me/drive/items/${parentFolderId}/children`,
        {
          name: folderName,
          folder: {},
          '@microsoft.graph.conflictBehavior': 'rename'
        },
        {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log(`📁 Created folder: ${folderName}`);
      return response.data.id;
    } catch (error) {
      console.error(`❌ Failed to create folder ${folderName}:`, error.response?.data || error.message);
      throw error;
    }
  }
}

async function loadFolderMapping() {
  try {
    const configFile = await fs.readFile('folder-mapping.yml', 'utf8');
    const config = yaml.load(configFile);
    
    // Debug: log the loaded configuration
    console.log('📋 Loaded configuration:');
    console.log('   Mappings:', Object.keys(config.mappings || {}).length);
    console.log('   Include patterns:', config.include_patterns);
    console.log('   Exclude patterns:', config.exclude_patterns);
    
    // Validate configuration structure
    if (!config.mappings) {
      throw new Error('Configuration missing "mappings" section');
    }
    
    if (Object.keys(config.mappings).length === 0) {
      throw new Error('No folder mappings defined in configuration');
    }
    
    if (!config.include_patterns) {
      console.log('⚠️  No include_patterns found, using default: **/*.md');
      config.include_patterns = ['**/*.md'];
    }
    
    if (!config.exclude_patterns) {
      console.log('ℹ️  No exclude_patterns found, using empty array');
      config.exclude_patterns = [];
    }
    
    return config;
  } catch (error) {
    console.error('❌ Failed to load folder mapping:', error.message);
    throw error;
  }
}

function getFolderMapping(filePath, mappings) {
  // Extract the first directory from the file path
  const pathParts = filePath.split(path.sep);
  const firstDir = pathParts[0];
  
  // Check if there's a mapping for this folder
  if (mappings.mappings[firstDir]) {
    return {
      folderId: mappings.mappings[firstDir],
      folderName: firstDir
    };
  }
  
  // No mapping found - return null to indicate we should skip this file
  return null;
}

async function findMarkdownFiles(config) {
  const allFiles = [];
  
  // Ensure include_patterns is an array
  const includePatterns = Array.isArray(config.include_patterns) 
    ? config.include_patterns 
    : [config.include_patterns || '**/*.md'];
    
  // Ensure exclude_patterns is an array
  const excludePatterns = Array.isArray(config.exclude_patterns)
    ? config.exclude_patterns
    : (config.exclude_patterns ? [config.exclude_patterns] : []);
  
  console.log(`🔍 Include patterns: ${includePatterns.join(', ')}`);
  console.log(`🚫 Exclude patterns: ${excludePatterns.join(', ')}`);
  
  // Find files matching include patterns
  for (const pattern of includePatterns) {
    try {
      const files = await glob(pattern, { nodir: true });
      console.log(`📁 Pattern "${pattern}" found ${files.length} files`);
      allFiles.push(...files);
    } catch (error) {
      console.warn(`⚠️  Error with pattern "${pattern}":`, error.message);
    }
  }
  
  // Remove duplicates
  const uniqueFiles = [...new Set(allFiles)];
  console.log(`📄 Found ${uniqueFiles.length} unique files before filtering`);
  
  // Filter out excluded files
  const filteredFiles = uniqueFiles.filter(file => {
    return !excludePatterns.some(excludePattern => {
      try {
        // Use glob's minimatch function for pattern matching
        const { minimatch } = require('minimatch');
        return minimatch(file, excludePattern);
      } catch (error) {
        console.warn(`⚠️  Error matching exclude pattern "${excludePattern}":`, error.message);
        return false;
      }
    });
  });
  
  console.log(`✅ Final file count after exclusions: ${filteredFiles.length}`);
  
  return filteredFiles;
}

async function main() {
  try {
    // Get environment variables
    const clientId = process.env.ONEDRIVE_CLIENT_ID;
    const clientSecret = process.env.ONEDRIVE_CLIENT_SECRET;
    const refreshToken = process.env.ONEDRIVE_REFRESH_TOKEN;
    
    if (!clientId || !clientSecret || !refreshToken) {
      throw new Error('Missing required environment variables: ONEDRIVE_CLIENT_ID, ONEDRIVE_CLIENT_SECRET, ONEDRIVE_REFRESH_TOKEN');
    }

    console.log('🚀 Starting OneDrive upload process...');
    
    // Load folder mapping configuration
    const config = await loadFolderMapping();
    console.log(`📋 Loaded folder mapping with ${Object.keys(config.mappings).length} mappings`);
    
    // Initialize uploader
    const uploader = new OneDriveUploader(clientId, clientSecret, refreshToken);
    
    // Find all markdown files
    const markdownFiles = await findMarkdownFiles(config);
    console.log(`📄 Found ${markdownFiles.length} markdown files to upload`);
    
    if (markdownFiles.length === 0) {
      console.log('ℹ️ No markdown files found to upload');
      return;
    }
    
    // Upload each file
    let successCount = 0;
    let errorCount = 0;
    let skippedCount = 0;
    
    for (const filePath of markdownFiles) {
      try {
        const mapping = getFolderMapping(filePath, config);
        
        // Skip files that don't have a folder mapping
        if (!mapping) {
          console.log(`⏭️  Skipped: ${filePath} (no folder mapping found)`);
          skippedCount++;
          continue;
        }
        
        const fileName = path.basename(filePath);
        
        console.log(`📤 Uploading: ${filePath} → ${mapping.folderName}/${fileName}`);
        
        await uploader.uploadFile(filePath, mapping.folderId, fileName);
        successCount++;
      } catch (error) {
        console.error(`❌ Failed to upload ${filePath}:`, error.message);
        errorCount++;
      }
    }
    
    console.log(`\n📊 Upload Summary:`);
    console.log(`   ✅ Successful uploads: ${successCount}`);
    console.log(`   ⏭️  Skipped files: ${skippedCount}`);
    console.log(`   ❌ Failed uploads: ${errorCount}`);
    console.log(`   📄 Total files processed: ${markdownFiles.length}`);
    
    if (errorCount > 0) {
      process.exit(1);
    }
    
  } catch (error) {
    console.error('💥 Fatal error:', error.message);
    process.exit(1);
  }
}

// Run the script
if (require.main === module) {
  main();
}

module.exports = { OneDriveUploader, loadFolderMapping, getFolderMapping };