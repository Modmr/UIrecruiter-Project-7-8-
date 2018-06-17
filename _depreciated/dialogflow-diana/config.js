export default {
    app: {
        token: "be72d4a27ad74a288cf3ba3d16fbdacc",//token: "9d686a47b1de48bab431e94750d1cd87", // <- enter your token here
        muted: false, // <- mute microphone by default
        watermark: false // <- show watermark
    },
    locale: {
        strings: {
            welcomeTitle: "Hello, ask something to get started",
            welcomeDescription: `You can type "Hello" for example. Or just press on the microphone to talk`,
            offlineTitle: "Oh, no!",
            offlineDescription: "It looks like you are not connected to the internet, this webpage requires internet connection, to process your requests",
            queryTitle: "Ask me something...",
            voiceTitle: "Go ahead, im listening..."
        },
        settings: {
            speechLang: "en-ZA", // <- output language
            recognitionLang: "en-US" // <- input(recognition) language
        }
    }
}