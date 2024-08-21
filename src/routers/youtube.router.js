const express = require('express');
const Youtube = require('../models/youtube.model');
const youtubeRouter = express.Router();

youtubeRouter.get('/', async (req, res) => {
    try {
        const youtubes = await Youtube.find();
        res.render('index', { youtubes });  // EJS 템플릿에 데이터를 전달
    } catch (error) {
        console.error(error);
        res.status(500).send('Server Error');
    }
});

youtubeRouter.get('/:id', async(req, res) => {
    try {
        const youtubes = await Youtube.findById(req.params.id);
        if (!youtubes) {
            return res.status(404).json({ message: 'Not found' });
        }
        res.render('detail', { youtubes });
    } catch (error) {
        console.error(error);
        res.status(500).send('Server Error');
    }
});

youtubeRouter.get('/search/search', async(req, res) => {
    try {
        const search = req.query.query || '검색 결과 없음';
        let youtubes = [];

        if (search !== '검색 결과 없음') {
            youtubes = await Youtube.find({
                $or: [
                    { title: { $regex: search, $options: 'i' } }
                ]
            });
        }

        res.render('search', { youtubes, queryValue: search });
    } catch (error) {
        console.error(error);
        res.status(500).send('Server Error');
    }
});


module.exports = youtubeRouter;