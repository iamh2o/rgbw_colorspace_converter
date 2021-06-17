<script>
  import {status, seconds_remaining} from './stores';
</script>

{#if $status.show}
  <span>running <strong>{$status.show}</strong> : {$seconds_remaining} seconds remaining</span>
{:else}
  <span><em>...loading</em></span>
{/if}
