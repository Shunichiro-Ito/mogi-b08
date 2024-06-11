<script>

    import { onMount, beforeUpdate } from 'svelte';

    //今日の日付データを変数に格納
    //変数は"today"とする
    let today=new Date(); 

    //年・月・日・曜日を取得
    let year = today.getFullYear();
    let month = today.getMonth()+1;
    let week = today.getDay();
    let day = today.getDate();

    let week_ja= new Array("日","月","火","水","木","金","土");

    //年・月・日・曜日を書き出す
   //document.write(year+"年"+month+"月"+day+"日 "+week_ja[week]+"曜日");

   //変数は"time"とする
    //let time= new Date();

    //時・分・秒を取得
    let hour;
    let minute;
    let second;
    onMount(async () => {

    function showclock(){
      let nowtime=new Date(); 
      hour = nowtime.getHours();
      minute = nowtime.getMinutes();
      second = nowtime.getSeconds();

    }
    showclock();
    setInterval(showclock,1000);
    })
  //document.write(hour+"時",+minute+"分"+second+"秒");
  </script>
  
   
    <header><p class="blue">BlueNetwork</p></header>
      <p class="date">現在時刻 : {year}年{month}/{day}日({week_ja[week]}) {hour}時{minute}分{second}秒</p>
      <!--<p class="time">{hour}時{minute}分{second}秒</p>-->
    <h1>違反者位置情報</h1>
    <p>aa</p>
    <p>bb</p>
    <p>cc</p>
    <footer>違反者取締アプリ~BlueNetwork~</footer>
  
  
  <style>
    header {
      height:10%;
      align-items: center;
      background: linear-gradient(to right, blue, pink);
      margin-bottom: 0;
    }

    h1 {
      text-align: center;
      border-bottom: solid 3px;
      border-left:solid 3px;
      border-right:solid 3px;
      margin-top: 0;
      margin-bottom: 0;
    }

    .blue {
      text-align: center;
      font-family: "Poetsen One", sans-serif;
      font-weight: 400;
      font-style: normal;
    }

    .date {
      text-align: center;
      border: solid 3px;
      margin-top: 0;
      margin-bottom: 0;
      padding: 1%;
    }

   footer{
    text-align: center;
    background-color: blue;
    height:10%;
    font-family: "Poetsen One", sans-serif;
    font-weight: 400;
    font-style: normal;
    color: aliceblue;

   }
  
  </style>