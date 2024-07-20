<script>
  import { onMount } from "svelte";

  let violations = [];
  //violationsは最初はonmountでページを開いた瞬間に全データリクエストのクエリが送られ、全データが代入されるが、検索ボックスのボタンクリックイベント
  //で新たにリクエストしてきたデータをviolationsにまた代入すれば、htmlの部分はviolationsだけ書いておけば勝手に変わる

  // 全データ取得
  const fetchViolations = async () => {
    const response = await fetch("http://localhost:8000/violations/");
    violations = await response.json();
    console.log("Violations:", violations); // データをログに出力
  };

  // ダミー生成リクエスト
  const generateDummyData = async () => {
    const response = await fetch("http://localhost:8000/generate_dummy_data/", {
      method: "POST",
    });

    if (response.ok) {
      // fetchViolations();
    } else {
      console.error("Failed to generate dummy data");
    }
  };

  // ダミーデータ削除
  const deleteDummyData = async () => {
    const response = await fetch("http://localhost:8000/delete_dummy_data/", {
      method: "DELETE",
    });

    if (response.ok) {
      // fetchViolations();
    } else {
      console.error("Failed to delete dummy data");
    }
  };

   //websocket
   export const ws = new WebSocket("ws://localhost:8000/ws");
  ws.onmessage = (event) => {
    // メッセージ受信時処理(データ表示を行う)
    const message = event.data;
    console.log(message);
    fetchViolations();
  };

  onMount(() => {
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

  //チェックボックスまとめたもの
  let filters = {
    checkBox1: false,
    checkBox2: false,
    //checkBox3: false,
    //dateRange: '',
  };

  //プルダウン
  let questions = [
    { id: 1, text: "question1" },
    { id: 2, text: "question2" },
    { id: 3, text: "question3" },
  ];
  let selected;

  // 検索ボタンを押したときの関数
  async function search() {
    const response = await fetch("http://localhost:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(filters),
    });
    violations = await response.json();
  }
</script>

<h1>違反者データベース</h1>
<div>
  <button on:click={generateDummyData}>Add Dummy Data</button>
  <button on:click={deleteDummyData}>Delete Dummy Data</button>
</div>

<main>
  <div class="kensaku">
    <!--チェックボックス(カメラ番号)-->
    <p>カメラ番号</p>
    <label>
      <input type="checkbox" bind:checked={filters.checkBox1} />
      カメラ1
    </label>
    <br />
    <label>
      <input type="checkbox" bind:checked={filters.checkBox2} />
      カメラ2
    </label>
    <br />

    <!--チェックボックス(違反内容)-->
    <p>違反内容</p>
    <label>
      <input type="checkbox" />
      傘さし運転
    </label>
    <br />

    <!--プルダウン-->
    <p>日時</p>
    <select bind:value={selected}>
      {#each questions as question}
        <option value={question}>
          {question.text}
        </option>
      {/each}
    </select>

    <!--検索ボックス-->
    <button on:click={search}>検索</button>
  </div>

  <table>
    <thead>
      <tr>
        <th>日付</th>
        <th>カメラ番号</th>
        <th>違反内容</th>
        <th>写真</th>
      </tr>
    </thead>
    <tbody>
      {#each violations as violation}
        <tr>
          <td>{violation.date}</td>
          <td>{violation.cam_no}</td>
          <td>{violation.violation}</td>
          <td>
            {#if violation.image}
              <img
                src={`data:image/png;base64,${violation.image}`}
                alt="Violation Image"
              />
            {/if}
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</main>

<style>
  h1 {
    text-align: center;
    font-family: "Noto Serif JP", serif;
    border-bottom: solid 3px;
    margin-top: 0;
    margin-bottom: 0;
  }

  main {
    text-align: center;
    margin: 0 auto;
    max-width: 600px;
    display: flex;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
  }

  th {
    background-color: #f2f2f2;
  }

  img {
    max-width: 100%;
    height: auto;
  }
</style>
