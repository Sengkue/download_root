import express from 'express';
import { getLinks, createLink, deleteLink, updateLink } from '../controllers/webview.controller.js';

const router = express.Router();

router.get('/', getLinks);
router.post('/', createLink);
router.delete('/:id', deleteLink);
router.put('/:id', updateLink);

export default router;
