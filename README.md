# py-powermenu

**Power menu for Linux based in ArchCraft power menu.**

After migrating from ArchCraft to Ubuntu, I tried to reuse all the good toys of the previous distro. But the power menu was not working. There was an undiscovered issue with the **if** statement in **bash** script deciding the "YES" or "NO" answer to the question of powering off, shutting down, or logging of menu. So, I decided to implement it in Python, using some recently adquired knowledge of functional programming (monads).
