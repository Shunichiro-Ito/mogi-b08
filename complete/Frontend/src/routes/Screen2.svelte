<script>
  import { onMount } from "svelte";

  const BASE_URL = "/api";

  let violations = [];
  //violationsは最初はonmountでページを開いた瞬間に全データリクエストのクエリが送られ、全データが代入されるが、検索ボックスのボタンクリックイベント
  //で新たにリクエストしてきたデータをviolationsにまた代入すれば、htmlの部分はviolationsだけ書いておけば勝手に変わる

  // 全データ取得
  const fetchViolations = async () => {
    const response = await fetch(BASE_URL + "/violations/");
    violations = await response.json();
    //violations.date = formatDateTime(violations.date)
    console.log("Violations:", violations); // データをログに出力
  };

  // ダミー生成リクエスト
  const generateDummyData = async () => {
    const response = await fetch(BASE_URL + "/generate_dummy_data/", {
      method: "POST",
    });

    if (response.ok) {
      fetchViolations();
    } else {
      console.error("Failed to generate dummy data");
    }
  };

  // ダミーデータ削除
  const deleteDummyData = async () => {
    const response = await fetch(BASE_URL + "/delete_dummy_data/", {
      method: "DELETE",
    });

    if (response.ok) {
      fetchViolations();
    } else {
      console.error("Failed to delete dummy data");
    }
  };

  onMount(() => {
    fetchViolations();
  });

  //チェックボックスまとめたもの
  let filters = {
    checkBox1: false,
    checkBox2: false,
    checkBox3: false,
    checkBox4: false,
    checkBox5: false,
    checkBox6: false,
    startDateTime: "",
    endDateTime: "",
  };

  //プルダウン
  let startDate = "";
  let startTime = "";
  let endDate = "";
  let endTime = "";

  // 検索ボタンを押したときの関数
  async function search() {
    filters.startDateTime =
      startDate && startTime ? `${startDate}T${startTime}` : "";
    filters.endDateTime = endDate && endTime ? `${endDate}T${endTime}` : "";
    const response = await fetch(BASE_URL + "/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(filters),
    });
    violations = await response.json();
    //violations.date = formatDateTime(violations.date)
  }

  // Tを取り除き、小数点以下を削除する関数
  function formatDateTime(dateandtime) {
    dateandtime += 9 * 60 * 1000
    // "T"で分割
    let [date, time] = dateandtime.split('T');
    // 秒の部分の小数点以下を削除
    time = time.split('.')[0];
    return `${date} ${time}`;
  }
</script>

<h1>違反者データベース</h1>
<div>
  <button on:click={generateDummyData}>Add Dummy Data</button>
  <button on:click={deleteDummyData}>Delete Dummy Data</button>
</div>

<main>
  <div class="kensaku">
    <h2>条件絞り込み</h2>

    <!--プルダウン-->
    <p class="attribute">日時</p>
    <div>
      <label>From: Date</label>
      <input type="date" bind:value={startDate} />
      <label>Time</label>
      <input type="time" bind:value={startTime} />
    </div>
    <div>
      <label>To: Date</label>
      <input type="date" bind:value={endDate} />
      <label>Time</label>
      <input type="time" bind:value={endTime} />
    </div>

    <!--チェックボックス(カメラ番号)-->
    <p class="attribute">カメラ番号</p>
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
    <label>
      <input type="checkbox" bind:checked={filters.checkBox3} />
      カメラ1かつ2
    </label>

    <!--チェックボックス(違反内容)-->
    <p class="attribute">違反内容</p>
    <label>
      <input type="checkbox" bind:checked={filters.checkBox4} />
      傘さし運転
    </label>
    <br />
    <label>
      <input type="checkbox" bind:checked={filters.checkBox5} />
      スマホ運転
    </label>
    <br />
    <label>
      <input type="checkbox" bind:checked={filters.checkBox6} />
      二人乗り運転
    </label>
    <br />

    <!--検索ボックス-->
    <button on:click={search} class="retrieve">検索</button>
  </div>

  <table>
    <thead>
      <tr>
        <th>日時</th>
        <th>カメラ番号</th>
        <th>違反内容</th>
        <th>写真</th>
      </tr>
    </thead>
    <tbody>
      {#each violations as violation}
        <tr>
          <td>{formatDateTime(violation.date)}</td>
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
    border-left: solid 3px;
    border-right: solid 3px;
    margin-top: 0;
    margin-bottom: 0;
  }

  main {
    text-align: center;
    max-width: 1200px;
    display: flex;
  }

  p {
    margin: 3%;
  }

  .attribute {
    border-bottom: solid;
    font-weight: bold;
    margin-top: 5%;
  }

  .kensaku {
    width: 30%;
    margin-right: 10%;
  }

  .retrieve {
    width: 50%;
    margin-top: 10%;
    background-color: blue;
    color: #f2f2f2;
  }

  table {
    width: 90%;
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
    /* width: 100%; */
    height: 50%;
  }

  img:hover {
    width: 80%;
    height: 100%;
  }
</style>
