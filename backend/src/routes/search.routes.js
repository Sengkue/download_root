import express from 'express';
import { searchImages } from '../controllers/search.controller.js';

const router = express.Router();

router.get('/', searchImages);

export default router;
