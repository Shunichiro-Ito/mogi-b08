<script>
    import { onMount } from 'svelte';
  
    let violations = [];
  
    const fetchViolations = async () => {
      const response = await fetch('http://localhost:8000/violations/');
      violations = await response.json();
      console.log('Violations:', violations); // データをログに出力
    };
  

    const generateDummyData = async () => {
      const response = await fetch('http://localhost:8000/generate_dummy_data/', {
        method: 'POST'
      });
  
      if (response.ok) {
        // fetchViolations();
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
        // fetchViolations();
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
    });

  </script>
  
  <main>
    <h1>Violation List</h1>
    <div>
      <button on:click="{generateDummyData}">Add Dummy Data</button>
      <button on:click="{deleteDummyData}">Delete Dummy Data</button>
    </div>
    <h2>Violations List:</h2>
    <ul>
      {#each violations as violation}
        <li>
          <p>Camera No: {violation.cam_no}</p>
          <p>Date: {violation.date}</p>
          <p>Violator: {violation.violation}</p>
          {#if violation.image}
            <img src={`data:image/png;base64,${violation.image}`} alt="" />
          {/if}
        </li>
      {/each}
    </ul>
  </main>
  
  <style>
    main {
      text-align: center;
      margin: 0 auto;
      max-width: 600px;
    }
    img {
      max-width: 100%;
      height: auto;
    }
  </style>
  