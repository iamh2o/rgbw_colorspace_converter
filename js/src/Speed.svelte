<script>
  import {onMount} from 'svelte';
  import Slider from '@smui/slider';

  // MDCSlider has bug with floats < 1, so use percentages
  let value = 100;

  onMount(async () => {
    const resp = await fetch('speed');
    if (!resp.ok) {
      throw new Error('failed to get /speed');
    }
    const data = await resp.json();
    value = data['value']*100;
  });

  const handleChange = async (e, v) => {
    await fetch('speed', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({value: value/100}),
    });
  };
</script>

<div class="flex flex-col m-1 text-white">
  Speed Percentage
  <Slider min={50} max={200} step={25} discrete bind:value on:MDCSlider:change={handleChange} />
</div>
