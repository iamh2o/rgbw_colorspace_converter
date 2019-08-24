<TailwindCss/>
<main>
  <div class="w-full fixed top-0">
    <nav class="bg-pink-700 p-3 text-lg text-white">
      Triangle Shows | <Status />
    </nav>
  </div>

  <div class="mt-20 grid grid-cols-1 md:grid-cols-2 gap-4 m-4">
    <div class="col-span-1">
        <ShowSelector />
    </div>
    <div class="col-span-1">
      <GlobalSettings />
      <Playlist />
      <PlayingSettings />
    </div>
  </div>
</main>

<script>
  import GlobalSettings from './GlobalSettings.svelte';
  import Playlist from './Playlist.svelte';
  import PlayingSettings from './PlayingSettings.svelte';
  import ShowSelector from './ShowSelector.svelte';
  import Status from './Status.svelte';
  import TailwindCss from './TailwindCss.svelte';
</script>
