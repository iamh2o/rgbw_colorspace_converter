<script>
  import {playlist} from './stores';
  import PlaylistItem from './PlaylistItem.svelte';
</script>

<div class="bg-gray-800 rounded-md p-2 mt-1">
  <div class="flex justify-between items-center">
    <h5 class="text-lg text-white my-2">Playlist</h5>
    <div>
      <button class="bg-black p-1 rounded-md text-white" on:click={playlist.clear}>
        Reset
      </button>
    </div>

  </div>

  <ul class="divide-y divide-gray-700">
    {#each $playlist.playlist as [entryId, show]}
      <PlaylistItem entryId={entryId} show={show} />
    {/each}
  </ul>
</div>
