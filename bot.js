const TelegramBot = require('node-telegram-bot-api');
const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

// Токенро аз environment variables гир
const token = process.env.TELEGRAM_TOKEN;

// Агар токен вуҷуд надошта бошад
if (!token) {
    console.error('❌ TELEGRAM_TOKEN not found!');
    process.exit(1);
}

const bot = new TelegramBot(token, { polling: true });

// Барои нигоҳ доштани сервер фаъол
app.get('/', (req, res) => {
    res.send('✅ Bot is running on Railway!');
});

// Фаъолияти бот
bot.onText(/\/start/, (msg) => {
    bot.sendMessage(msg.chat.id, 'Салом! Бот дар Railway кор мекунад 🚀');
});

bot.on('message', (msg) => {
    if (msg.text && !msg.text.startsWith('/')) {
        bot.sendMessage(msg.chat.id, `Шумо навиштед: "${msg.text}"`);
    }
});

// Серверро оғоз кун
app.listen(PORT, () => {
    console.log(`🚀 Bot started on port ${PORT}`);
    console.log(`✅ Bot is active!`);
});
