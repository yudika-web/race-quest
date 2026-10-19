const {run,fixture}=require('./reuse.cjs');run('test_export.cjs',s=>{
 for(const id of ['p','q'])s=s.replaceAll("await "+id+".locator('#characterGrid [data-index=\"1\"]').click();","await "+id+".locator('#characterNext').click();await "+id+".locator('#characterGrid [data-index=\"8\"]').click();");
 return s.replace('await p.goto(',fixture+'await p.goto(').replace('await q.goto(',fixture.replaceAll('p.addInitScript','q.addInitScript')+'await q.goto(');
});
