<script>
  import chroma from 'chroma-js';

  // props
  export let name, value = {}, onChange;

  // input type="color" uses RGB values, so convert to/from HSV
  let hsv = value.setting || value.default;
  let colorValue = chroma({h: hsv.h*360, s: hsv.s, v: hsv.v}).hex('rgb');

  const onChangeRGB = () => {
    const [h,s,v] = chroma(colorValue).hsv();
    onChange({h:h/360, s:s, v:v})
  }
</script>

<label class="flex flex-col m-1 text-white">
  {name}
  <input class="my-2" type="color" bind:value={colorValue} on:change={onChangeRGB} />
</label>
