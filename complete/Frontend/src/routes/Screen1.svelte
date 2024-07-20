<script>
    import { onMount } from 'svelte';

    // 表示データ読み込み
    let jsonData = {};
    let videoWin, videoDesk;

    // JSONデータの例
    onMount(async () => {
        jsonData = await fetch('https://api.example.com/data')
            .then(response => response.json())
            .catch(error => console.error('Error fetching JSON data:', error));
    });

     /******************** Streaming  *******************************/
     function startStream() {
        const imgWindow = document.createElement('img');
        imgWindow.src = "http://blue-network.eolstudy.com/cam-window";
        imgWindow.alt = "Video Stream";
        imgWindow.style.width = "100%";
        imgWindow.style.height = "auto";
        videoWin.appendChild(imgWindow);

        const imgDesk = document.createElement('img');
        imgDesk.src = "http://blue-network.eolstudy.com/cam-desk";
        imgDesk.alt = "Video Stream";
        imgDesk.style.width = "100%";
        imgDesk.style.height = "auto";
        videoDesk.appendChild(imgDesk);
    }

    /******************** OnMount *******************************/
    onMount(() => {
      // ストリーミング受信処理
      startStream();
    });
</script>

  <div class="grid-container">
    <div class="grid-item">
      <div id="video-win" bind:this={videoWin}></div> <!--とりあえずwebカメラの映像表示-->
        <!-- <video controls autoplay>
          <source src={videoUrls[0]} type="application/x-mpegURL">
          Your browser does not support the video tag.
        </video> -->
    </div>
    <div class="grid-item">
      <div id="video-desk" bind:this={videoDesk}></div>
    </div>
    <div class="grid-item json-display">
      <pre>{JSON.stringify(jsonData, null, 2)}</pre>
    </div>
  </div>

  <style>
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
      height: auto;
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