<script>
    import { onMount } from 'svelte';

    // 表示データ読み込み
    let videoUrls = ["stream1.m3u8", "stream2.m3u8", "stream3.m3u8"];
    let jsonData = {};

    // JSONデータの例
    onMount(async () => {
        jsonData = await fetch('https://api.example.com/data')
            .then(response => response.json())
            .catch(error => console.error('Error fetching JSON data:', error));
    });
</script>

<h1>リアルタイム違反者情報</h1>
<div class="grid-container">
    <div class="grid-item">
        <video controls autoplay>
            <source src={videoUrls[0]} type="application/x-mpegURL">
            Your browser does not support the video tag.
        </video>
    </div>
    <div class="grid-item">
        <video controls autoplay>
            <source src={videoUrls[1]} type="application/x-mpegURL">
            Your browser does not support the video tag.
        </video>
    </div>
    <div class="grid-item">
        <video controls autoplay>
            <source src={videoUrls[2]} type="application/x-mpegURL">
            Your browser does not support the video tag.
        </video>
    </div>
    <div class="grid-item json-display">
        <pre>{JSON.stringify(jsonData, null, 2)}</pre>
    </div>
</div>

<style>
    h1 {
        text-align: center;
        border-bottom: solid 3px;
        border-left: solid 3px;
        border-right: solid 3px;
        margin-top: 0;
        margin-bottom: 0;
    }

    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        gap: 10px;
        padding: 10px;
    }

    .grid-item {
        border: 2px solid #ccc;
        padding: 10px;
    }

    video {
        width: 100%;
        height: 100%;
    }

    .json-display {
        overflow: auto;
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 5px;
    }

    pre {
        margin: 0;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
</style>
