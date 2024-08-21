const express = require('express');
const app = express()
const PORT = process.env.PORT || 3000
const { YoutubeTranscript } = require('youtube-transcript');
const OpenAI = require('openai');

const openai = new OpenAI({
    apiKey: process.env.API_KEY
})

async function getVideoId(url) {
    try {
        video_id = await url.split('?v=')[1];
        return video_id
    } catch (error) {
        console.error("Error parsing URL:", error);
    }
}

async function getTranscript(videoId) {
    try {
        const transcript = await YoutubeTranscript.fetchTranscript(videoId, { lang: 'ko'})
         // text 속성만 추출
        const texts = transcript.map(item => item.text);
        
         // 추출한 text를 출력
        return texts.join(' ');
    } catch (error) {
        console.error("Error fetching transcript:", error);
    }
}

async function getSummary(text) {
    const thread = await openai.beta.threads.create();
    const message = await openai.beta.threads.messages.create(thread.id, {
        role: 'user',
        content: text
    })

    let run = await openai.beta.threads.runs.create(thread.id, {
        assistant_id: process.env.ASSISTANT_ID
    })

    console.log(run.id)

    while (true) {
        run = await openai.beta.threads.runs.retrieve(thread.id, run.id);
        if (run.status == 'completed') {
            break
        } else {
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }

    const threadMessages = await openai.beta.threads.messages.list(thread.id);
    return threadMessages.data[0].content[0].text.value;
}

async function main() {
    try {
        const videoId = await getVideoId("https://www.youtube.com/watch?v=dKKRwe8DPw8")
        const text = await getTranscript(videoId);
        console.log(text);
        const summary = await getSummary(text);
        console.log(summary);
    } catch (error) {
        console.error(error)
    }
}

main();

app.listen(PORT, () => console.log(`Listening on ${PORT}`))