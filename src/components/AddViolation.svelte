<!-- frontend/src/components/AddViolation.svelte -->

<script>
    import { createEventDispatcher } from 'svelte';
    import axios from 'axios';

    const dispatch = createEventDispatcher();

    let camNo;
    let date;
    let violator;

    async function addViolation() {
        try {
            await axios.post('http://localhost:8000/violations/', {
                cam_no: camNo,
                date: Date.parse(date) / 1000,  // Unixエポックに変換
                violator: violator
            });
            dispatch('violationAdded');
            camNo = '';
            date = '';
            violator = '';
        } catch (error) {
            console.error('Error adding violation:', error);
        }
    }
</script>

<h2>Add Violation</h2>

<label for="camNo">Camera Number:</label>
<input type="number" id="camNo" bind:value={camNo}>

<label for="date">Date:</label>
<input type="date" id="date" bind:value={date}>

<label for="violator">Violator:</label>
<input type="text" id="violator" bind:value={violator}>

<button on:click={addViolation}>Add Violator</button>
