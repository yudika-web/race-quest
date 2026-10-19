require('./reuse.cjs').run('test_offline.cjs',s=>s.replace('if(require.main===module)','if(true)'));
