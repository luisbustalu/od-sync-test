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
      
      // First, try to upload the file
      const uploadUrl = `https://graph.microsoft.com/v1.0/me/drive/items/${folderId}:/${fileName}:/content`;
      
      const response = await axios.put(uploadUrl, fileContent, {
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'text/markdown'
        }
      });

      console.log(`✅ Uploaded: ${fileName} to folder ${folderId}`);
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
    return yaml.load(configFile);
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
  
  // Return default folder
  return {
    folderId: mappings.default_folder_id,
    folderName: 'default'
  };
}

async function findMarkdownFiles(config) {
  const allFiles = [];
  
  // Find files matching include patterns
  for (const pattern of config.include_patterns) {
    const files = await glob(pattern, { nodir: true });
    allFiles.push(...files);
  }
  
  // Remove duplicates
  const uniqueFiles = [...new Set(allFiles)];
  
  // Filter out excluded files
  const filteredFiles = uniqueFiles.filter(file => {
    return !config.exclude_patterns.some(excludePattern => {
      // Use glob's minimatch function for pattern matching
      const { minimatch } = require('minimatch');
      return minimatch(file, excludePattern);
    });
  });
  
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
    
    for (const filePath of markdownFiles) {
      try {
        const mapping = getFolderMapping(filePath, config);
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