<script>
  import {status} from './stores';
  import HSVKnob from './HSVKnob.svelte';
  import ValueKnob from './ValueKnob.svelte';

  const changeSettingCallback = (show, name) => {
    return async (value) => {
      await fetch('show_knob', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({show: show, name: name, value: value}),
      });
    };
  };
</script>

{#if $status.showKnobs.length !== 0}
<div class="bg-gray-800 rounded-md p-2 mt-1">
  <h5 class="text-lg text-white my-2">Now Playing - {$status.show}</h5>
  <em class="text-sm text-white my-1">Note: affects running show and choices are not saved</em>

  <ul>
    {#each $status.showKnobs as knob}
      <li>
        {#if knob.type === 'HSVKnob'}
        <HSVKnob {...knob} onChange={changeSettingCallback($status.show, knob.name)} />
        {:else if knob.type === 'ValueKnob'}
        <ValueKnob {...knob} onChange={changeSettingCallback($status.show, knob.name)} />
        {/if}
      </li>
    {/each}
  </ul>
</div>
{/if}
