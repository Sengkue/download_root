import { DataTypes } from 'sequelize';
import { sequelize } from '../config/database.js';

export const TypingHistory = sequelize.define('TypingHistory', {
  userId: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  lessonTitle: {
    type: DataTypes.STRING,
    allowNull: false
  },
  wpm: {
    type: DataTypes.INTEGER,
    allowNull: false,
    defaultValue: 0
  },
  cpm: {
    type: DataTypes.INTEGER,
    allowNull: false,
    defaultValue: 0
  },
  accuracy: {
    type: DataTypes.FLOAT,
    allowNull: false,
    defaultValue: 0
  },
  timeSeconds: {
    type: DataTypes.STRING,
    allowNull: true
  }
});
