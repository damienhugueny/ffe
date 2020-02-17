

console.log('coucou')

const express = require('express')
const puppeteer = require('puppeteer')

var app = express();

let port = 8080;
 
app.get('/:p1', function(req, res) { // création de la route sous le verbe get
    
    var p1 = req.params.p1;
 console.log(p1);
    p1 = p1.replace( /\+/, " ",)
    p1 = p1.replace( /\+/, " ",)
console.log(p1);

    void(async() => {
        try{
            const browser = await puppeteer.launch()
    
            const page = await browser.newPage()
    
    
            await page.goto('https://ffecompet.ffe.com/cheval', {waitUntil: 'networkidle2'});
    
            await page.type('#horse_name', p1);
            //on click sur le bouton radion qui a l'id horse...
            await page.click(
                '#horse_critSearchNameHorse_critSearchName_0',
              )
    
            //await page.$eval('input[name=search]', el => el.value = 'Adenosine triphosphate');
    
            await page.click('button[type="submit"]');
    
            
    
            // 3 - Récupérer les données
            const result = await page.evaluate(() => {
            let info = document.querySelector('#horse-detail-div').innerText
            info = info.split("\n");
            return {info}
      })

            let json = JSON.stringify(result)
            console.log(json)
            res.send(json)// envoi de hello world a l'utilisateur

            await browser.close()
            
            return result
            
            
        } catch(error){
            console.log(error)
        }
    })()











})
 
 
app.listen(port, () =>  { // ecoute du serveur sur le port 8080
    console.log('le serveur fonctionne')
})








 
/*
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
  
    await page.goto('https://ffecompet.ffe.com/cheval');
  
    //await page.waitFor('input[horse_name=BEBE RAPH ERCA]')
   // await page.type('#horse_name', 'BEBE RAPH ERCA');
    //await page.keyboard.press('Enter');
  
    //await page.click('input[type="submit"]');
    await page.waitForNavigation();

    await page.screenshot({
        path: './screenshots/page1.png'
    })

    await page.screenshot({
        path: './screenshots/page1.png'
    })
    //console.log('New Page URL:', page.url());
    await browser.close();
  })();*/
