const {run,fixture}=require('./reuse.cjs');run('test_game.cjs',s=>{
 s=s.replace("await page.locator('#characterGrid [data-index=\"1\"]').click();","await page.locator('#characterNext').click();await page.locator('#characterGrid [data-index=\"11\"]').click();")
    .replace("await mobile.locator('#characterGrid [data-index=\"3\"]').click();","await mobile.locator('#characterNext').click();await mobile.locator('#characterNext').click();await mobile.locator('#characterGrid [data-index=\"12\"]').click();")
    .replaceAll('data-index="1"','data-index="11"').replaceAll('kart_nara','kart_panda')
    .replaceAll('New penguin','New panda').replaceAll('Blocky penguin','Blocky panda');
 return s.replace('await page.goto(',fixture.replaceAll('p.addInitScript','page.addInitScript')+'await page.goto(').replace('await mobile.goto(',fixture.replaceAll('p.addInitScript','mobile.addInitScript')+'await mobile.goto(');
});
