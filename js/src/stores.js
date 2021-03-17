import {derived, readable, writable} from 'svelte/store';

// lastUpdate is a timestamp of the last /status update. It lets us countdown remaining show time.
let lastUpdate = new Date();

// status is a readable store which periodically updates itself
export const status = readable({show: undefined, seconds: 0, showKnobs: []},
  function start(set) {
    const interval = setInterval(async () => {
      const resp = await fetch('status');
      if (!resp.ok) {
        throw new Error('get /status failed');
      }
      const { show, seconds_remaining, knobs } = await resp.json();

      set({
        show: show,
        seconds: seconds_remaining,
        showKnobs: knobs,
      });

      lastUpdate = new Date();
    }, 2000);
    return () => clearInterval(interval);
});

// seconds_remaining is a readable store decrementing down to zero.
// The counter resets when status store is updated.
export const seconds_remaining = derived(
  status,
  ($status, set) => {
    const interval = setInterval(() => {
      const elapsed = Math.round((new Date() - lastUpdate) / 1000);
      const remaining = $status.seconds - elapsed;
      set(remaining >= 0 ? remaining : 0);
    }, 500);
    return () => clearInterval(interval);
});

// createPlaylist creates a writeable store for playlist data.
// Rather than using the raw store, it returns several methods for interacting with the playlist.
function createPlaylist() {
  const latest = async () => {
    const resp = await fetch('playlist');
    if (!resp.ok) {
      throw new Error('get /playlist failed');
    }
    return await resp.json();
  };

  let initialValue = {'playlist':[],'playing':undefined};
  const { subscribe, set, update } = writable(initialValue,
    function start(set) {
      // updates playlist data from server on an interval
      const interval = setInterval(async () => {
        const data = await latest();
        set(data);
      }, 1000);
      return () => clearInterval(interval);
  });

  const clear = async () => {
    await fetch('playlist', {
      method: 'DELETE',
    });
    set(initialValue);
  };

  const add = async (show) => {
    const resp = await fetch('playlist', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({show: show}),
    });
    if (!resp.ok) {
      throw new Error('failure adding to playlist');
    }
    const data = await resp.json();
    set(data);
  }

  const deleteItem = async (entryId) => {
    const resp = await fetch(`playlist/entries/${entryId}`, {
      method: 'DELETE',
    });
    if (!resp.ok) {
      throw new Error(`failure to DELETE playlist entry playlist/entries/${entryId}`);
    }
    const data = await latest();
    set(data);
  };

  const setNext = async (entryId) => {
    await fetch('playlist', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({entry_id: entryId}),
    });
    update(data => {
      data.playing = entryId;
      return data;
    });
  };

  return {
    subscribe, // subscribe is necessary for all stores
    clear,
    add,
    deleteItem,
    setNext,
  };
}

export const playlist = createPlaylist();
