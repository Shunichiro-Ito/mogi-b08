<!-- frontend/src/components/ViolationsList.svelte -->

<script>
    import { onMount } from 'svelte';
    import axios from 'axios';

    let violations = [];

    async function fetchViolations() {
        try {
            let response = await axios.get('http://localhost:8000/violations/');
            violations = response.data;
        } catch (error) {
            console.error('Error fetching violations:', error);
        }
    }

    onMount(fetchViolations); // コンポーネントがマウントされた時に一覧を取得

    // イベントリスナーの登録
    window.addEventListener('violationAdded', () => {
        fetchViolations();
    });
</script>

<h2>Violations List</h2>

<ul>
    {#each violations as violation}
        <li>{violation.violator} - {violation.cam_no} - {new Date(violation.date * 1000).toLocaleDateString()}</li>
    {/each}
</ul>
