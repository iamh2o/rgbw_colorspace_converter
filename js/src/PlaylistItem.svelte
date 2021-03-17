<script>
  import {onMount} from 'svelte';
  import {playlist} from './stores';

  import Icon from 'svelte-awesome';
  import {chevronRight, cog, trash} from "svelte-awesome/icons";

  import Dialog, {Content, Title} from '@smui/dialog';
  import HSVKnob from './HSVKnob.svelte';
  import ValueKnob from './ValueKnob.svelte';

  // props
  export let entryId, show;

  let settingsDialog;
  let showKnobs = [];

  // load the available knobs and any settings for the show
  onMount(async () => {
    let resp = await fetch(`show_knob/${show}`);
    if (!resp.ok) {
      throw new Error(`get show_knob/${show} failed`);
    }
    const showKnobData = await resp.json();

    resp = await fetch(`playlist/entries/${entryId}`);
    if (!resp.ok) {
      throw new Error('failed getting settings for playlist entry');
    }
    const settings = await resp.json();
    showKnobData.forEach((knob) => {
      knob.value.setting = settings[knob.name];
    });

    showKnobs = showKnobData;
  });

  // returns a function to change the setting
  const changeSettingCallback = (name) => {
    return async (value) => {
      const resp = await fetch(`playlist/entries/${entryId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ [name]: value }),
      });
      if (!resp.ok) {
        throw new Error(`failed to POST setting to playlist/entries/${entryId}`);
      }
    };
  };
</script>

<div>
  <Dialog bind:this={settingsDialog}>
    <Title>{show} Settings</Title>
    <Content>
      <ul>
        {#each showKnobs as knob}
          <li>
            {#if knob.type === 'HSVKnob'}
            <HSVKnob {...knob} onChange={changeSettingCallback(knob.name)} />
            {:else if knob.type === 'ValueKnob'}
            <ValueKnob {...knob} onChange={changeSettingCallback(knob.name)} />
            {/if}
          </li>
        {/each}
      </ul>
    </Content>
  </Dialog>

  <div class="rounded-md flex justify-between items-center p-1 ripple-bg-gray-800 text-white"
   on:click|self={() => playlist.setNext(entryId)}>
    <div class="flex"> <!-- Icon and show name to the left -->
      <div class="w-4">
        {#if $playlist.playing === entryId}
        <Icon data={chevronRight}/>
        {/if}
      </div>
      {show}
    </div>
    <div class="flex"> <!-- Icon buttons to the right -->
      {#if showKnobs.length}
      <div class="m-1" on:click={settingsDialog.open}>
        <Icon data={cog} scale="2"/>
      </div>
      {/if}
      <div class="m-1" on:click={() => playlist.deleteItem(entryId)}>
        <Icon data={trash} scale="2"/>
      </div>
    </div>
  </div>
</div>
