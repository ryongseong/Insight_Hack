const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const YoutubeSchema = new Schema({
    title: String,
    channel_name: String,
    description: String,
    thumbnail: String,
    source_url: {
        type: String,
        required: true
    },
    summary: String
})

const Youtubes = mongoose.model('Youtube', YoutubeSchema);

module.exports = Youtubes