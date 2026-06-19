import { DataTypes } from 'sequelize';
import { sequelize } from '../config/database.js';

export const WebviewLink = sequelize.define('WebviewLink', {
  title: {
    type: DataTypes.STRING,
    allowNull: false
  },
  url: {
    type: DataTypes.STRING,
    allowNull: false
  }
});
