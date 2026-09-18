import { sequelize } from './src/config/database.js';
import TikTokChannel from './src/models/TikTokChannel.js';

async function cleanup() {
  try {
    await sequelize.authenticate();
    const result = await TikTokChannel.destroy({
      where: { channelId: 'test_user_123' }
    });
    console.log(`Deleted ${result} mock channel(s).`);
  } catch (error) {
    console.error('Error during cleanup:', error);
  } finally {
    process.exit(0);
  }
}

cleanup();
