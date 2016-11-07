var app = angular.module('webTess', ['chart.js'])
.controller('formCtrl', function($scope, $http){

    $scope.formData = {};
    $scope.tables=false;
    $scope.message= 'Enter Text to Evaluate...';
    $scope.posgraph=false;
    $scope.descgraph=false;
    $scope.freqgraph=false;
    $scope.mrcgraph=false;


    $scope.processForm = function() {
      $scope.tables = false;
      $scope.message = 'Loading...';
      $http({
            method : 'POST',
            url : '/main',
            data : $.param($scope.formData),
            headers : { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
            })
            .then(function(response){
              $scope.data= response.data;
              $scope.tables=true;
              $scope.descgraph=false;
              $scope.posgraph=false;
              $scope.freqgraph=false;
              $scope.mrcgraph=false;
              $scope.descGraph();
              $scope.posGraph();
              $scope.freqGraph();
              $scope.mrcGraph();
              // $scope.message='Data Recieved, But not doing anything';
            },
                function(error) {
                  $scope.message='Please Enter a Valid Passage...';
                  $scope.tables=false;
                  $scope.descgraph=false;
                  $scope.posgraph=false;
                  $scope.freqgraph=false;
                  $scope.mrcgraph=false;
                  console.log(error);
                }
            );
          };

    $scope.sentProcess = function() {
      $scope.simcnt = 'Loading...';
      $http({
            method : 'POST',
            url : '/sent',
            data : $.param($scope.formData),
            headers : { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
            })
            .then(function(response){
              $scope.sentdata = response.data;
              $scope.simcnt = $scope.sentdata.simval;
            }, function(error){
              $scope.simcnt = 'Error in Getting Similarity';
              console.log(error);
            });
          };

          // $scope.passProcess = function() {
          //
          //   alert("this may take upto 2 min");
          //   $scope.simcnt = 'Loading...';
          //   $http({
          //         method : 'POST',
          //         url : 'http://127.0.0.1:5000/pass',
          //         data : $.param($scope.formData),
          //         headers : { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
          //         })
          //         .then(function(response){
          //           $scope.passdata = response.data;
          //           $scope.simcnt = $scope.passdata.simval;
          //           $scope.formData.p1sim = $scope.passdata.p1sim
          //           $scope.formData.p2sim = $scope.passdata.p2sim
          //           $scope.formData.simpassage = $scope.passdata.simpassage
          //
          //
          //         });
          //       };

    $scope.wordProcess = function() {
      $http({
            method : 'POST',
            url : '/word',
            data : $.param($scope.formData),
            headers : { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }
          })
            .then(function(response){
              $scope.worddata= response.data;
              $scope.wordaoa = $scope.worddata.age;
              $scope.wfguide = $scope.worddata.sfivalue + '\n\n' + $scope.worddata.grade1 + '\n' + $scope.worddata.grade2 + '\n' + $scope.worddata.grade3 + '\n' + $scope.worddata.grade4 + '\n' + $scope.worddata.grade5 + '\n' + $scope.worddata.grade6 + '\n' + $scope.worddata.grade7 + '\n' + $scope.worddata.grade8 + '\n' + $scope.worddata.grade9 + '\n' + $scope.worddata.grade10 + '\n' + $scope.worddata.grade11 + '\n' + $scope.worddata.grade12 + '\n' + $scope.worddata.grade13;
              $scope.errorword = '';
            },
              function(error) {
                $scope.errorword = '(Please Enter a Valid Word)';
                $scope.worddata = '';
                $scope.wordaoa = '';
                console.log(error);
              }

          );
          };


    $scope.filetext = function(contents) {
        // console.log(contents);
        $scope.formData.passage = contents;
    };

    $scope.$watch('formData.enterword', function()
    {
      if ($scope.formData.enterword == "") {
          $scope.clearword();
      }
      else {
          $scope.wordProcess();
      }

    });


    $scope.sam1 = function() {
      $scope.formData.passage = 'Assyria comprised the area now known as Iraq. As the empire expanded from the Mediterranean in the west to the Persian Gulf in the east, the means of travel were improved, largely for military use. Roads were improved, markers were established to indicate distances, and posts and wells were developed for safety and nourishment. Even today we see the influence of military construction aiding pleasure travel.\n\tThe recently completed United States interstate highway system was developed initially to facilitate transportation in the event of a national emergency. Assyrian military traveled by chariot, others by horse, while the donkey was the principal mode of transportation of the common people.  The Persians, who defeated the Assyrians, continued improvements in the travel infrastructure. New kinds of wagons were developed including a four-wheeled carriage for the wealthy.';
    };

    $scope.sam2 = function() {
      $scope.formData.passage = 'Mammoths reigned as giants on land for more than three million years. Many were as tall as a house and weighed as much as a semi truck. Their huge ivory tusks dipped and curved to a length of 10 feet (3 meters). Adult mammoths feared no predators—except perhaps humans.\n\tMost mammoths lived during the Pleistocene epoch—a span of time when long periods of intense cold were occasionally interrupted by shorter cycles of warmer weather. The Pleistocene epoch ended about eleven thousand years ago. By that time, the mammoths had nearly vanished. Extinction claimed these Ice-Age giants.\n\tMammoths and dinosaurs shared a similar fate. They were among the largest animals on land, and extinction wiped out both of them. But that\'s pretty much where the similarity ends. Dinosaurs became extinct millions of years before mammoths arrived on the scene. Unlike the reptilian dinosaurs, mammoths were mammals and, for a while, they coexisted with humans. Like mice, muskrats, horses, hares, and other modern mammals, mammoths gave birth to their young and nursed their babies with mother\'s milk.\n\tScientists know more about the physical appearance and lifestyle of mammoths than they do about dinosaurs because abundant, well-preserved mammoth remains have been discovered. These include frozen carcasses—complete with skin, hair, and internal organs, including the heart. Researchers have also uncovered intact mammoth skeletons buried on land and bones submerged in the sea. They have even pieced together what the giant animals ate by studying mammoth dung found in caves. So far, mammoth remains have been found only on the continents of Africa, Europe, Asia, and North America. No signs of mammoths have been discovered in the Southern Hemisphere.\n\tBy studying mammoth remains paleontologists (scientists who study evidence of past life on Earth) have learned that many different kinds of mammoths roamed the Northern Hemisphere. There were the woolly mammoths whose hairy overcoats offered warm protection from the arctic cold. There were the larger, less hairy Columbian mammoths that favored the warmer climate of North America. There were even island-dwelling miniature mammoths.\n\tScientists have learned a great deal by studying mammoth remains, but that is not their only source of knowledge. Ancient peoples who lived alongside mammoths also left behind clues. Cave paintings—some in surprising detail—captured the first human observations of mammoths. In addition, ancient artifacts reveal that humans used mammoth bones and tusks as tools and for ornamentation. They even built entire huts out of mammoth bones.\n\tThere is plenty of evidence that humans hunted the great mammoths. However, the question remains: How did mammoths become extinct? Did humans hunt the Ice-Age giants to extinction? Perhaps the mammoths were killed by Earth\'s changing climate or by disease, or perhaps something else—something scientists don\'t yet know about—was responsible. Scientists would also like to know why elephants, close relatives of the mammoths, continue to survive, while mammoths died out.\n\tSo far, researchers have not been able to solve any of these mysteries. That is why they continue to probe for clues.';
    };


    $scope.clear = function() {
      $scope.formData.passage = '';
      $scope.tables=false;
      $scope.posgraph=false;
      $scope.descgraph=false;
      $scope.freqgraph=false;
      $scope.message='Enter Text to Evaluate...';
      $scope.errorword = '';
      $scope.data='';
      $scope.clearword();
      $scope.clearsim();
    };

    $scope.clearword = function() {
        $scope.formData.enterword = '';
        $scope.wordaoa = '';
        $scope.errorword = '(Enter a Word)';
        $scope.worddata='';
    };

    $scope.clearsim = function() {
        $scope.formData.p1sim = '';
        $scope.formData.p2sim = '';
        $scope.simcnt = '';
    };

        Chart.defaults.global.defaultFontColor = 'rgba(151,187,205,0.2)';
        $scope.colours1 = [
          { // green
              fillColor: "rgba(70,191,189,0.2)",
              strokeColor: "rgba(70,191,189,1)",
              pointColor: "rgba(70,191,189,1)",
              pointStrokeColor: "#fff",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(70,191,189,0.8)"
          },
          { // dark grey
              fillColor: "rgba(77,83,96,0.2)",
              strokeColor: "rgba(77,83,96,1)",
              pointColor: "rgba(77,83,96,1)",
              pointStrokeColor: "#fff",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(77,83,96,1)"
          },
          { // blue
              fillColor: "rgba(151,187,205,0.2)",
              strokeColor: "rgba(151,187,205,1)",
              pointColor: "rgba(151,187,205,1)",
              pointStrokeColor: "#fff",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(151,187,205,0.8)"
          },
          { // light grey
              fillColor: "rgba(220,220,220,0.2)",
              strokeColor: "rgba(220,220,220,1)",
              pointColor: "rgba(220,220,220,1)",
              pointStrokeColor: "#fff",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(220,220,220,0.8)"
          },

          { // red
              fillColor: "rgba(247,70,74,0.2)",
              strokeColor: "rgba(247,70,74,1)",
              pointColor: "rgba(247,70,74,1)",
              pointStrokeColor: "#fff",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(247,70,74,0.8)"
          },
    { // yellow
        fillColor: "rgba(253,180,92,0.2)",
        strokeColor: "rgba(253,180,92,1)",
        pointColor: "rgba(253,180,92,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(253,180,92,0.8)"
    },
    { // grey
        fillColor: "rgba(148,159,177,0.2)",
        strokeColor: "rgba(148,159,177,1)",
        pointColor: "rgba(148,159,177,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(148,159,177,0.8)"
    }
];



    $scope.descGraph = function() {
      $scope.char1 = 0;
      $scope.char2 = 0;
      $scope.char3 = 0;
      $scope.char4 = 0;
      $scope.char5 = 0;
      $scope.char6 = 0;
      $scope.char7 = 0;
      $scope.char8 = 0;
      $scope.char9 = 0;
      $scope.char10 = 0;
      $scope.char11 = 0;
      $scope.char12 = 0;
      $scope.char13 = 0;


      angular.forEach($scope.data.descriptive.wordlengths, function(value,key) {
          if(value.clength == 1)
              $scope.char1++;
          if(value.clength == 2)
              $scope.char2++;
          if(value.clength == 3)
              $scope.char3++;
          if(value.clength == 4)
              $scope.char4++;
          if(value.clength == 5)
              $scope.char5++;
          if(value.clength == 6)
              $scope.char6++;
          if(value.clength == 7)
              $scope.char7++;
          if(value.clength == 8)
              $scope.char8++;
          if(value.clength == 9)
              $scope.char9++;
          if(value.clength == 10)
              $scope.char10++;
          if(value.clength == 11)
              $scope.char11++;
          if(value.clength == 12)
              $scope.char12++;
          if(value.clength > 12)
              $scope.char13++;

      });
$scope.chardata = [$scope.char1,$scope.char2,$scope.char3,$scope.char4,$scope.char5,$scope.char6,$scope.char7,$scope.char8,$scope.char9,$scope.char10,$scope.char11,$scope.char12,$scope.char13];
$scope.charlabel = ['1','2','3','4','5','6','7','8','9','10','11','12','13+'];




$scope.syll1 = 0;
$scope.syll2 = 0;
$scope.syll3 = 0;
$scope.syll4 = 0;
$scope.syll5 = 0;
angular.forEach($scope.data.descriptive.wordlengths, function(value,key) {
    if(value.slength == 1)
        $scope.syll1++;
    if(value.slength == 2)
        $scope.syll2++;
    if(value.slength == 3)
        $scope.syll3++;
    if(value.slength == 4)
        $scope.syll4++;
    if(value.slength > 4)
        $scope.syll5++;

});
$scope.sylldata = [$scope.syll1,$scope.syll2,$scope.syll3,$scope.syll4,$scope.syll5];
$scope.sylllabel = ['1','2','3','4','5+'];
    };

    $scope.freqGraph = function() {
      $scope.sfi1 = 0;
      $scope.sfi2 = 0;
      $scope.sfi3 = 0;
      $scope.sfi4 = 0;
      $scope.sfi5 = 0;

      angular.forEach($scope.data.wordfreq.sfiwords, function(value,key) {
          if(value.sfi <= 20)
              $scope.sfi1++;
          else if(value.sfi <= 40)
              $scope.sfi2++;
          else if(value.sfi <= 60)
              $scope.sfi3++;
          else if(value.sfi <= 80)
              $scope.sfi4++;
          else if(value.sfi <= 100)
              $scope.sfi5++;
      });
      $scope.freqlabel = ['SFI 0-20','SFI 21-40','SFI 41-60','SFI 61-80','SFI 81-100'];
      $scope.freqdata = [$scope.sfi1,$scope.sfi2,$scope.sfi3,$scope.sfi4,$scope.sfi5];
    };

    $scope.mrcGraph = function() {

      Chart.defaults.global.colours = [
    { // blue
        fillColor: "rgba(151,187,205,0.1)",
        strokeColor: "rgba(151,187,205,1)",
        pointColor: "rgba(151,187,205,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(151,187,205,0.8)"
    },

    { // red
        fillColor: "rgba(247,70,74,0.1)",
        strokeColor: "rgba(247,70,74,1)",
        pointColor: "rgba(247,70,74,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(247,70,74,0.8)"
    },
    { // green
        fillColor: "rgba(70,191,189,0.1)",
        strokeColor: "rgba(70,191,189,1)",
        pointColor: "rgba(70,191,189,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(70,191,189,0.8)"
    },
    { // yellow
        fillColor: "rgba(253,180,92,0.1)",
        strokeColor: "rgba(253,180,92,1)",
        pointColor: "rgba(253,180,92,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(253,180,92,0.8)"
    },
    { // brown
        fillColor: "rgba(178,38,0,0.1)",
        strokeColor: "rgba(178,38,0,1)",
        pointColor: "rgba(178,38,0,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(178,38,0,1)"
    },
    { // grey
        fillColor: "rgba(148,159,177,0.1)",
        strokeColor: "rgba(148,159,177,1)",
        pointColor: "rgba(148,159,177,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(148,159,177,0.8)"
    },
    { // light grey
        fillColor: "rgba(220,220,220,0.1)",
        strokeColor: "rgba(220,220,220,1)",
        pointColor: "rgba(220,220,220,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(220,220,220,0.8)"
    },
];

      $scope.aoa1 = 0;
      $scope.aoa2 = 0;
      $scope.aoa3 = 0;
      $scope.aoa4 = 0;
      $scope.aoa5 = 0;
      $scope.aoa6 = 0;
      $scope.aoa7 = 0;
      angular.forEach($scope.data.mrc.dictionary, function(value,key) {
        if(value.aoa !='*') {
            if(value.aoa <= 200)
                $scope.aoa1++;
            else if(value.aoa <= 300)
                $scope.aoa2++;
            else if(value.aoa <= 400)
                $scope.aoa3++;
            else if(value.aoa <= 500)
                $scope.aoa4++;
            else if(value.aoa <= 600)
                $scope.aoa5++;
            else if(value.aoa <= 700)
                $scope.aoa6++;
            else if(value.aoa > 700)
                $scope.aoa7++;
        }
      });

      $scope.fam1 = 0;
      $scope.fam2 = 0;
      $scope.fam3 = 0;
      $scope.fam4 = 0;
      $scope.fam5 = 0;
      $scope.fam6 = 0;
      $scope.fam7 = 0;
      angular.forEach($scope.data.mrc.dictionary, function(value,key) {
        if(value.fam !='*') {
            if(value.fam <= 200)
                $scope.fam1++;
            else if(value.fam <= 300)
                $scope.fam2++;
            else if(value.fam <= 400)
                $scope.fam3++;
            else if(value.fam <= 500)
                $scope.fam4++;
            else if(value.fam <= 600)
                $scope.fam5++;
            else if(value.fam <= 700)
                $scope.fam6++;
            else if(value.fam > 700)
                $scope.fam7++;
        }
      });


      $scope.imag1 = 0;
      $scope.imag2 = 0;
      $scope.imag3 = 0;
      $scope.imag4 = 0;
      $scope.imag5 = 0;
      $scope.imag6 = 0;
      $scope.imag7 = 0;
      angular.forEach($scope.data.mrc.dictionary, function(value,key) {
        if(value.imag !='*') {
            if(value.imag <= 200)
                $scope.imag1++;
            else if(value.imag <= 300)
                $scope.imag2++;
            else if(value.imag <= 400)
                $scope.imag3++;
            else if(value.imag <= 500)
                $scope.imag4++;
            else if(value.imag <= 600)
                $scope.imag5++;
            else if(value.imag <= 700)
                $scope.imag6++;
            else if(value.imag > 700)
                $scope.imag7++;
        }
      });

      $scope.conc1 = 0;
      $scope.conc2 = 0;
      $scope.conc3 = 0;
      $scope.conc4 = 0;
      $scope.conc5 = 0;
      $scope.conc6 = 0;
      $scope.conc7 = 0;
      angular.forEach($scope.data.mrc.dictionary, function(value,key) {
        if(value.conc !='*') {
            if(value.conc <= 200)
                $scope.conc1++;
            else if(value.conc <= 300)
                $scope.conc2++;
            else if(value.conc <= 400)
                $scope.conc3++;
            else if(value.conc <= 500)
                $scope.conc4++;
            else if(value.conc <= 600)
                $scope.conc5++;
            else if(value.conc <= 700)
                $scope.conc6++;
            else if(value.conc > 700)
                $scope.conc7++;
        }
      });


      $scope.mean1 = 0;
      $scope.mean2 = 0;
      $scope.mean3 = 0;
      $scope.mean4 = 0;
      $scope.mean5 = 0;
      $scope.mean6 = 0;
      $scope.mean7 = 0;
      angular.forEach($scope.data.mrc.dictionary, function(value,key) {
        if(value.mean !='*') {
            if(value.mean <= 200)
                $scope.mean1++;
            else if(value.mean <= 300)
                $scope.mean2++;
            else if(value.mean <= 400)
                $scope.mean3++;
            else if(value.mean <= 500)
                $scope.mean4++;
            else if(value.mean <= 600)
                $scope.mean5++;
            else if(value.mean <= 700)
                $scope.mean6++;
            else if(value.mean > 700)
                $scope.mean7++;
        }
      });

      $scope.mrcseries = ['Age of Aquisition','Familiarity','Imagibility','Concreteness','Meaningfulness'];
      $scope.mrclabel = ['0-200','201-300','301-400','401-500','501-600','601-700','700+'];
      $scope.mrcdata = [
        [$scope.aoa1,$scope.aoa2,$scope.aoa3,$scope.aoa4,$scope.aoa5,$scope.aoa6,$scope.aoa7],
        [$scope.fam1,$scope.fam2,$scope.fam3,$scope.fam4,$scope.fam5,$scope.fam6,$scope.fam7],
        [$scope.imag1,$scope.imag2,$scope.imag3,$scope.imag4,$scope.imag5,$scope.imag6,$scope.imag7],
        [$scope.conc1,$scope.conc2,$scope.conc3,$scope.conc4,$scope.conc5,$scope.conc6,$scope.conc7],
        [$scope.mean1,$scope.mean2,$scope.mean3,$scope.mean4,$scope.mean5,$scope.mean6,$scope.mean7],
      ];

      $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
  $scope.mrcoptions = {
    scales: {
      yAxes: [
        {
          id: 'y-axis-1',
          type: 'linear',
          display: true,
          position: 'left'
        },
        {
          id: 'y-axis-2',
          type: 'linear',
          display: true,
          position: 'right'
        }
      ]
    }
  };





    };



    $scope.posGraph = function() {


      $scope.lexlabels = [['NN','NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG','VBN','VBP','VBZ','JJ','JJR','JJS','RB','RBR','RBS'],['Noun, singular or mass', ' Noun, plural', 'Proper Noun, singular', 'Proper Noun, plural', 'Verb, base form', 'Verb, past tense', 'Verb, gerund/present participle','Verb, past participle','Verb, non-3rd person singular','Verb, 3rd person singular','Adjective','Adjective, comparative','Adjective, superlative','Adverb','Adverb, comparative','Adverb, superlative']];
      $scope.lexseries = ['Lexical Part of Speech'];
      lexi=0;
      $scope.lexchart_options = {
        tooltipTemplate: function(label) {
          return label.label + ' : ' + label.value;
          lexi++;
        }
      };
      $scope.lexdata = [
        [$scope.data.pos.lex.nn.count,$scope.data.pos.lex.nns.count,$scope.data.pos.lex.nnp.count,$scope.data.pos.lex.nnps.count,$scope.data.pos.lex.vb.count,$scope.data.pos.lex.vbd.count,$scope.data.pos.lex.vbg.count,$scope.data.pos.lex.vbn.count,$scope.data.pos.lex.vbp.count,$scope.data.pos.lex.vbz.count,$scope.data.pos.lex.jj.count,$scope.data.pos.lex.jjr.count,$scope.data.pos.lex.jjs.count,$scope.data.pos.lex.rb.count,$scope.data.pos.lex.rbr.count,$scope.data.pos.lex.rbs.count]
      ];




      $scope.nonlexlabels = [['PRP', 'PRP$', 'DT', 'CC', 'IN', 'RP', 'TO','CD','EX','FW','MD','PDT','POS','UH','WDT','WP','WP$','WRB'],['Personal Pronoun','Possessive Pronoun','Determiner','Coordinating Conjunction','Preposition','Particle','to','Cardinal Number','Existential There','Foreign Word','Modal','Predeterminer','Possessive Ending','Interjection','Wh-Determiner','Wh-Pronoun','Possessive Wh-Pronoun','Wh-Adverb']];
      $scope.nonlexseries = ['Non-Lexical Part of Speech'];
      $scope.nonlexdata = [
        [$scope.data.pos.nonlex.prp.count,$scope.data.pos.nonlex.prp$.count,$scope.data.pos.nonlex.dt.count,$scope.data.pos.nonlex.cc.count,$scope.data.pos.nonlex.in.count,$scope.data.pos.nonlex.rp.count,$scope.data.pos.nonlex.to.count,$scope.data.pos.nonlex.cd.count,$scope.data.pos.nonlex.ex.count,$scope.data.pos.nonlex.fw.count,$scope.data.pos.nonlex.md.count,$scope.data.pos.nonlex.pdt.count,$scope.data.pos.nonlex.pos.count,$scope.data.pos.nonlex.uh.count,$scope.data.pos.nonlex.wdt.count,$scope.data.pos.nonlex.wp.count,$scope.data.pos.nonlex.wp$.count,$scope.data.pos.nonlex.wrb.count]
      ];


      $scope.totallex = $scope.data.pos.lex.nn.count*1+$scope.data.pos.lex.nns.count*1+$scope.data.pos.lex.nnp.count*1+$scope.data.pos.lex.nnps.count*1+$scope.data.pos.lex.vb.count*1+$scope.data.pos.lex.vbd.count*1+$scope.data.pos.lex.vbg.count*1+$scope.data.pos.lex.vbn.count*1+$scope.data.pos.lex.vbp.count*1+$scope.data.pos.lex.vbz.count*1+$scope.data.pos.lex.jj.count*1+$scope.data.pos.lex.jjr.count*1+$scope.data.pos.lex.jjs.count*1+$scope.data.pos.lex.rb.count*1+$scope.data.pos.lex.rbr.count*1+$scope.data.pos.lex.rbs.count*1;
      $scope.totalnonlex = $scope.data.pos.nonlex.prp.count*1+$scope.data.pos.nonlex.prp$.count*1+$scope.data.pos.nonlex.dt.count*1+$scope.data.pos.nonlex.cc.count*1+$scope.data.pos.nonlex.in.count*1+$scope.data.pos.nonlex.rp.count*1+$scope.data.pos.nonlex.to.count*1+$scope.data.pos.nonlex.cd.count*1+$scope.data.pos.nonlex.ex.count*1+$scope.data.pos.nonlex.fw.count*1+$scope.data.pos.nonlex.md.count*1+$scope.data.pos.nonlex.pdt.count*1+$scope.data.pos.nonlex.pos.count*1+$scope.data.pos.nonlex.uh.count*1+$scope.data.pos.nonlex.wdt.count*1+$scope.data.pos.nonlex.wp.count*1+$scope.data.pos.nonlex.wp$.count*1+$scope.data.pos.nonlex.wrb.count*1;
      $scope.lexandnonlabel = ['Lexical Part of Speech','Non-Lexical Part of Speech'];
      $scope.lexandnondata =[$scope.totallex, $scope.totalnonlex];
};



})
.directive('onReadFile', function ($parse) {
    return {
        restrict: 'A',
        scope: false,
        link: function(scope, element, attrs) {
            element.bind('change', function(e) {

                var onFileReadFn = $parse(attrs.onReadFile);
                var reader = new FileReader();

                reader.onload = function() {
                    var fileContents = reader.result;
                    scope.$apply(function() {
                        onFileReadFn(scope, {
                            'contents' : fileContents
                        });
                    });
                };
                reader.readAsText(element[0].files[0]);
            });
        }
    };
});