<!-- App.svelte -->
<!-- npm installと npm run devでうごきます-->
<script>
    import { onMount } from 'svelte';

    let camNo;
    let date;
    let violator;
    let violations = [];

    async function addViolation() {
        try {
            const response = await fetch('http://localhost:8000/violations/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    cam_no: camNo,
                    date: date,
                    violator: violator
                })
            });

            if (!response.ok) {
                throw new Error('Failed to add violation');
            }

            await fetchViolations(); // 違反者一覧を更新
            // フォームをリセット
            camNo = '';
            date = '';
            violator = '';
        } catch (error) {
            console.error('Error adding violation:', error);
        }
    }

    async function fetchViolations() {
        try {
            const response = await fetch('http://localhost:8000/violations/');
            if (!response.ok) {
                throw new Error('Failed to fetch violations');
            }
            violations = await response.json();
        } catch (error) {
            console.error('Error fetching violations:', error);
        }
    }

    onMount(fetchViolations); // 初期表示時に一覧を取得

    // 違反者情報の削除（例示のためのサンプルコード）
    async function deleteViolation(id) {
        try {
            await axios.delete(`http://localhost:8000/violations/${id}`);
            await fetchViolations(); // 違反者一覧を更新
        } catch (error) {
            console.error('Error deleting violation:', error);
        }
    }
</script>

<h1>Violation Tracker</h1>

<!-- 違反者情報の追加フォーム -->
<h2>Add Violation</h2>

<label for="camNo">Camera Number:</label>
<input type="number" id="camNo" bind:value={camNo}>

<label for="date">Date:</label>
<input type="date" id="date" bind:value={date}>

<label for="violator">Violation:</label>
<input type="text" id="violator" bind:value={violator}>

<button on:click={addViolation}>Add Violator</button>

<!-- 違反者一覧 -->
<h2>Violations List</h2>

<ul>
    {#each violations as violation}
        <li>
            {violation.violator} - {violation.cam_no} - {violation.date}
            <button on:click={() => deleteViolation(violation.id)}>Delete</button>
        </li>
    {:else}
        <li>No violations found.</li>
    {/each}
</ul>
