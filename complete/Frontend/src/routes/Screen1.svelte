<script>
  import { onMount } from "svelte";

  // 表示データ読み込み
  let videoElement;

  //検知メッセージの表示
  let message;
  let visible = false;

  function DetectionMessage() {
    message = "違反者検出";
    visible = true;
    // 5秒後に非表示にする（例）
    setTimeout(() => {
      visible = false;
    }, 5000);
  }

  /******************** Websocket  *******************************/
  //export const ws = new WebSocket("ws://localhost:8000/ws");
  //ws.onmessage = (event) => {
  // メッセージ受信時処理(データ表示を行う)
  //const message = event.data;
  //console.log(message);
  //DetectionMessage();
  //};/

  /******************** Streaming  *******************************/
  function startStream() {
    const img = document.createElement("img");
    img.src = "/api/video_feed_yolo";
    img.alt = "Video Stream";
    img.style.width = "100%";
    img.style.height = "auto";
    videoElement.appendChild(img);
  }

  /******************** OnMount *******************************/
  onMount(() => {
    // ストリーミング受信処理
    startStream();

    const ws = new WebSocket("/api/ws");
    ws.onmessage = (event) => {
      // メッセージ受信時処理(データ表示を行う)
      const message = event.data;
      console.log(message);
      DetectionMessage();
    };

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  });
</script>

<h1>リアルタイム違反者情報</h1>

{#if visible}
  <div class="toast">
    <p>{message}</p>
  </div>
{/if}

<div class="realtime">
  <div class="camera1">カメラ1</div>

  <div class="camera2">カメラ2</div>

  <div id="videoContainer" bind:this={videoElement}></div>
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

  .realtime {
    position: relative;
  }

  .camera1 {
    position: absolute;
    background-color:blue;
    color: #fff;
    width:10%;
    text-align: center;
  }

  .camera2 {
    position: absolute;
    left: 50%;
    background-color:blue;
    color: #fff;
    width:10%;
    text-align: center;
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
