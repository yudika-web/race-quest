require('./reuse.cjs').run('test_core.cjs',s=>s.replace('b[2].body',"b.find(x=>x.body.includes('class Track')).body"));
