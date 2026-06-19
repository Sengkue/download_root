import { Sequelize } from 'sequelize';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize Sequelize with SQLite (File-based DB)
export const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: path.join(__dirname, '../../database.sqlite'),
  logging: false,
});

export const connectDB = async () => {
  try {
    await sequelize.authenticate();
    console.log('✅ SQLite Database connected successfully via Sequelize.');
    // Import models to ensure they are registered before sync
    await import('../models/User.js');
    await import('../models/Post.js');
    // Synchronize models
    await sequelize.sync();
  } catch (error) {
    console.error('❌ Unable to connect to the database:', error);
  }
};
