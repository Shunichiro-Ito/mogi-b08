<script>
  import { onMount } from 'svelte';
  import Screen1 from './Screen1.svelte';
  import Screen2 from './Screen2.svelte';

  // 今日の日付データを変数に格納
  let today = new Date();
  // 年・月・日・曜日を取得
  let year = today.getFullYear();
  let month = today.getMonth() + 1;
  let week = today.getDay();
  let day = today.getDate();
  let week_ja = ["日", "月", "火", "水", "木", "金", "土"];

  // 時・分・秒を取得
  let hour;
  let minute;
  let second;

  function twoDigit(num) {
    if( num < 10 )
      num = "0" + num;
    return num;
  }

  onMount(() => {
      function showclock() {
          let nowtime = new Date();
          hour = twoDigit(nowtime.getHours());
          minute = twoDigit(nowtime.getMinutes());
          second = twoDigit(nowtime.getSeconds());
      }
      showclock();
      setInterval(showclock, 1000);
  });

  // 現在表示している画面を管理する変数
  let currentScreen = 1;

  // 画面を切り替える関数
  function switchScreen(screen) {
      currentScreen = screen;
  }
</script>

<header><p class="title">BlueNetwork</p></header>

<nav>
  <button on:click={() => switchScreen(1)}>ライブ映像</button>
  <button on:click={() => switchScreen(2)}>違反記録</button>
  <span class="time">
    現在時刻 : {year}年{month}月{day}日({week_ja[week]}) {hour}時{minute}分{second}秒
  </span>
</nav>


<main>
{#if currentScreen === 1}
  <Screen1 />
{:else}
  <Screen2 />
{/if}
</main>

<footer>
  違反者取締アプリ~BlueNetwork~
</footer>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

  header {
    display: flex;
    justify-content: left;
    align-items: center;
    background: linear-gradient(to right, navy, blue);
    padding: 10px;
    height: 5%;
  }

  .title {
    font-family: 'Noto Serif JP', serif;
    font-weight: 500;
    font-size: 35pt;
    color: white;
  }

  nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f5f5f5;
    padding: 10px;
    border-bottom: 2px solid #ccc;
  }

  button {
    margin: 0 10px;
    padding: 10px 20px;
    font-size: 1em;
  }

  .time {
    margin-left: auto;
    font-family: "Roboto", sans-serif;
  }

  main {
    padding: 20px;
  }

  footer {
    text-align: center;
    background-color: navy;
    height: 7%;
    font-family: 'Roboto', sans-serif;
    font-weight: 400;
    color: aliceblue;
  }
</style>