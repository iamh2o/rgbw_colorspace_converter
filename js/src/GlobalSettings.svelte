<script>
  import Brightness from './Brightness.svelte';
  import ShowCycle from './ShowCycle.svelte';
  import Speed from './Speed.svelte';
</script>

<div class="bg-gray-800 rounded-md p-2">
  <h5 class="text-lg text-white my-2">Global Settings</h5>
  <div class="flex flex-col">
    <Brightness />
    <ShowCycle />
    <Speed />
  </div>
</div>
