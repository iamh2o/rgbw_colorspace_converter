<script>
  import {onMount} from 'svelte';
  import {playlist} from './stores';

  import Icon from 'svelte-awesome';
  import {playCircle, plusCircle} from "svelte-awesome/icons";

  let shows = [];

  onMount(async () => {
    const resp = await fetch('shows');
    if (!resp.ok) {
      throw new Error('get /shows failed');
    }
    const data = await resp.json();
    shows = data['shows'];
  });

  const clickPlay = async (show) => {
    await fetch('shows', {
      method: 'POST',
      body: JSON.stringify({data: show}),
      headers: {
        'Content-Type': 'application/json',
      },
    });
  };

  const clickEnqueue = async (show) => {
    await playlist.add(show);
  };

  let selected;
</script>

<div class="bg-gray-800 rounded-md p-2">
  <h5 class="text-lg text-white my-2">Show Selector</h5>

  <ul class="divide-y divide-gray-700">
    {#each shows as { name, description }}
      <li class="rounded-md flex justify-between items-center p-1">
        <div class="flex flex-col">
          <div class="text-white">{name}</div>
          <div class="text-sm text-gray-300">{description}</div>
        </div>
        <div class="flex"> <!-- Buttons -->
          <div class="m-1" on:click={() => clickPlay(name)}>
            <Icon class="text-white" data={playCircle} scale="2"/>
          </div>
          <div class="m-1" on:click={() => clickEnqueue(name)}>
            <Icon class="text-white" data={plusCircle} scale="2"/>
          </div>
        </div>
      </li>
    {/each}
  </ul>
</div>
