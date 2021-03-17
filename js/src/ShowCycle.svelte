<script>
  import {onMount} from 'svelte';
  import Slider from '@smui/slider';

  let value = 60;

  onMount(async () => {
    const resp = await fetch('cycle_time');
    if (!resp.ok) {
      throw new Error('failed to get /cycle_time');
    }
    const data = await resp.json();
    value = data['value'];
  });

  const handleChange = async (e, v) => {
    await fetch('cycle_time', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({value: value}),
    });
  };
</script>

<div class="flex flex-col m-1 text-white">
  Show duration (s)
  <Slider min={10} max={120} step={10} discrete bind:value on:MDCSlider:change={handleChange} />
</div>
