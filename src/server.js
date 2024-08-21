const express = require('express');
const { default: mongoose } = require('mongoose');
const path = require('path');
const bodyParser = require('body-parser');
const fs = require('fs');
const methodOverride = require('method-override');
const youtubeRouter = require('./routers/youtube.router');

require('dotenv').config();

const mongoURI = process.env.MONGO_URI;
const PORT = process.env.PORT;

const app = express();


app.use(express.json())
app.use(express.urlencoded({ extended: false }))
app.use(bodyParser.json());
app.use(methodOverride('_method'));

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(express.static(path.join(__dirname, 'public')));

app.use('/', youtubeRouter);

app.use((err, req, res, next) => {
    res.status(err.status || 500);
    res.send(err.message || '에러가 발생했습니다.')
})

mongoose.set('strictQuery', false);
mongoose.connect(mongoURI)
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));

const Youtube = require('./models/youtube.model');
const product_data = JSON.parse(fs.readFileSync(`${__dirname}/data/youtube_result.json`, 'utf-8'));

const importData = async () => {
    try {
        for (let data of product_data) {
            const exists = await Youtube.findOne({ source_url: data.source_url });

            if (!exists) {
                await Youtube.create({
                    title: data.title,
                    channel_name: data.channel_name,
                    description: data.description,
                    thumbnail: data.thumbnail,
                    source_url: data.source_url,
                    summary: ''
                });
            }
        }

        console.log('Data successfully created');
        process.exit();
    } catch (error) {
        console.log('Error', error);
        process.exit(1);
    }
}

// importData()

app.listen(PORT, () => console.log(`Listening on http://localhost:${PORT}`))
