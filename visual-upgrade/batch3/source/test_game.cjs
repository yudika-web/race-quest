const {run,fixture}=require('./reuse.cjs');run('test_game.cjs',s=>{
 s=s.replace("await page.locator('#characterGrid [data-index=\"1\"]').click();","await page.locator('#characterNext').click();await page.locator('#characterGrid [data-index=\"8\"]').click();")
    .replace("await mobile.locator('#characterGrid [data-index=\"3\"]').click();","await mobile.locator('#characterNext').click();await mobile.locator('#characterGrid [data-index=\"9\"]').click();")
    .replaceAll('data-index="1"','data-index="8"').replaceAll('kart_nara','kart_anjing')
    .replaceAll('New penguin','New dog').replaceAll('Blocky penguin','Blocky dog');
 return s.replace('await page.goto(',fixture.replaceAll('p.addInitScript','page.addInitScript')+'await page.goto(').replace('await mobile.goto(',fixture.replaceAll('p.addInitScript','mobile.addInitScript')+'await mobile.goto(');
});
