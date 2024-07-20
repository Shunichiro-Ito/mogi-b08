<script>
    import { onMount } from "svelte";

    const BASE_URL = 'http://localhost:8000'

    // 表示データ読み込み
    let videoElement;


    //検知メッセージの表示
    let message ;
    let visible = false;


    function DetectionMessage() {
        message = '違反者検出';
        visible = true;
        // 5秒後に非表示にする（例）
        setTimeout(() => {
            visible = false;
        }, 5000);
    }



    

    /******************** Streaming  *******************************/
    function startStream() {
        const img = document.createElement("img");
        img.src = BASE_URL + "/video_feed_yolo";
        img.alt = "Video Stream";
        img.style.width = "100%";
        img.style.height = "auto";
        videoElement.appendChild(img);
    }

    /******************** OnMount *******************************/
    onMount(() => {
        // ストリーミング受信処理
        startStream();
    });
</script>

<h1>リアルタイム違反者情報</h1>

{#if visible}
  <div class="toast">
    <p>{message}</p>
  </div>
{/if}

<div id="videoContainer" bind:this={videoElement}></div>

<style>
    h1 {
        text-align: center;
        border-bottom: solid 3px;
        border-left: solid 3px;
        border-right: solid 3px;
        margin-top: 0;
        margin-bottom: 0;
    }


    .toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #333;
    color: #fff;
    padding: 10px;
    border-radius: 4px;
    animation: slideIn 0.5s ease-out forwards;
  }

  @keyframes slideIn {
    from {
      transform: translateY(100%);
    }
    to {
      transform: translateY(0);
    }
  }
</style>
