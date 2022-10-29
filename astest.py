import asyncio,sys

async def do_thing(thing):
    proc = await asyncio.create_subprocess_shell(thing,stdout=asyncio.subprocess.PIPE)
    while proc.returncode is None:
        data = await proc.stdout.readline()
        if not data: break
        line = data.decode()
        # Handle line (somehow)
        print(line)

if sys.platform in ['win32','msys','cygwin']:
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

loop.run_until_complete(do_thing(sys.argv[1]))
loop.close()
