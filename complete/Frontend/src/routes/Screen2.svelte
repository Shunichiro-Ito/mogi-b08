<script>
    import { onMount } from 'svelte';
  
    let violations = [];
  
    // 全データ取得  
    const fetchViolations = async () => {
      const response = await fetch('http://localhost:8000/violations/');
      violations = await response.json();
      console.log('Violations:', violations); // データをログに出力
    };
  
    // ダミー生成リクエスト
    const generateDummyData = async () => {
      const response = await fetch('http://localhost:8000/generate_dummy_data/', {
        method: 'POST'
      });
  
      if (response.ok) {
        fetchViolations();
      } else {
        console.error('Failed to generate dummy data');
      }
    };

    // ダミーデータ削除
    const deleteDummyData = async () => {
      const response = await fetch('http://localhost:8000/delete_dummy_data/', {
        method: 'DELETE'
      });

      if (response.ok) {
        fetchViolations();
      } else {
        console.error('Failed to delete dummy data');
      }
    };
  
    /******************** WebSocket接続 *******************************/
    const ws = new WebSocket('ws://localhost:8000/ws');
    let messages = [];

    ws.onmessage = event => {
      // メッセージ受信時処理(データ表示を行う)
      const message = event.data;
      console.log(message)
      fetchViolations();
    };

    onMount(() => {
      ws.onopen = () => {
        console.log('WebSocket connected');
      };
      
      ws.onclose = () => {
        console.log('WebSocket closed');
      };

      ws.onerror = error => {
        console.error('WebSocket error:', error);
      };

      fetchViolations(); // ページロード時にデータを取得
    });
</script>

<main>
    <h1>違反者データベース</h1>
    <div>
      <button on:click="{generateDummyData}">ダミーデータ追加</button>
      <button on:click="{deleteDummyData}">ダミーデータ削除</button>
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
                <img src={`data:image/png;base64,${violation.image}`} alt="Violation Image" />
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
      font-family: 'Noto Serif JP', serif;
      border-bottom: solid 3px;
      margin-top: 0;
      margin-bottom: 0;
    }

    main {
      text-align: center;
      margin: 0 auto;
      max-width: 800px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    th, td {
      border: 1px solid #ddd;
      padding: 8px;
    }

    th {
      background-color: #f2f2f2;
    }

    img {
      max-width: 100px;
      height: auto;
    }
</style>