import { DataTypes } from 'sequelize';
import { sequelize } from '../config/database.js';

const YouTubeChannel = sequelize.define('YouTubeChannel', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  channelId: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  channelTitle: {
    type: DataTypes.STRING,
    allowNull: false
  },
  thumbnailUrl: {
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
  tableName: 'youtube_channels',
  timestamps: true
});

export default YouTubeChannel;
