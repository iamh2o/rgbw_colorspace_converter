<script>
  import Slider from '@smui/slider';

  // props
  export let name, value = {}, onChange;

  // MDCSlider has an annoying bug with floats < 1, so use percentages by multiplying by 100.
  let multiplier = (value.min === 0 && value.max === 1) ? 100 : 1;
  let min = value.min;
  let max = value.max * multiplier;
  let step = value.step * multiplier;
  let sliderValue = (value.setting || value.default) * multiplier;

  const submitChange = async () => {
    await onChange(sliderValue / multiplier);
  };
</script>

<div class="flex flex-col m-1 text-white">
  {name}
  <Slider min={min} max={max} step={step} discrete bind:value={sliderValue} on:MDCSlider:change={submitChange} />
</div>
