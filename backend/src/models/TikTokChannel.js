import { DataTypes } from 'sequelize';
import { sequelize } from '../config/database.js';

const TikTokChannel = sequelize.define('TikTokChannel', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  channelId: { // This will be the TikTok open_id or username
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  channelTitle: { // Display name
    type: DataTypes.STRING,
    allowNull: false
  },
  thumbnailUrl: { // Profile image
    type: DataTypes.STRING
  },
  accessToken: {
    type: DataTypes.TEXT,
    allowNull: false
  },
  refreshToken: {
    type: DataTypes.TEXT
  },
  tokenExpiry: {
    type: DataTypes.DATE
  }
}, {
  tableName: 'tiktok_channels',
  timestamps: true
});

export default TikTokChannel;
