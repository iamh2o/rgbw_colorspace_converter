<script>
  import {onMount} from 'svelte';
  import Slider from '@smui/slider';

  let value = 100;

  onMount(async () => {
    const resp = await fetch("brightness");
    if (!resp.ok) {
      throw new Error('failed to get /brightness');
    }
    const data = await resp.json();
    value = data.value;
  });

  const handleChange = async (e, v) => {
    await fetch('brightness', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({value: Math.round(value)}),
    });
  };
</script>

<div class="flex flex-col m-1 text-white">
  Brightness
  <Slider min={0} max={100} bind:value on:MDCSlider:change={handleChange} />
</div>
