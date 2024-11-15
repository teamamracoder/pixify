
const  allStories =[
    {
        id:0, 
        author:"sribash sarkar",
        profile:"static/images/p3.jpg",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:1,
        author:"PRIYA MITRA",
        imageUrl:"static/images/priya.jpg",
    },
    {
        id:2,
        author:"Rima das",
        imageUrl:"static/images/p2.jpg",
    },
    {
        id:3,
        author:"sribash sarkar",
        imageUrl:"static/images/p1.jpg",
    },
    {
        id:4,
        author:"sribash sarkar",
        imageUrl:"static/images/p2.jpg",
    },
    {
        id:5,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:6,
        author:"sribash sarkar",
        imageUrl:"static/images/p4.jpg",
    },
    {
        id:7,
        author:"sribash sarkar",
        imageUrl:"static/images/p5.jpg",
    },
    {
        id:0,
        author:"sribash sarkar",
        imageUrl:"static/images/p1.jpg",
    },
    {
        id:1,
        author:"sribash sarkar",
        imageUrl:"static/images/priya.jpg",
    },
    {
        id:2,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:3,
        author:"sribash sarkar",
        imageUrl:"static/images/priya.jpg",
    },
    {
        id:4,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:5,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:6,
        author:"sribash sarkar",
        imageUrl:"static/images/p4.jpg",
    },
    {
        id:7,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    }, 
    {
        id:0,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:1,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:2,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:3,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:4,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:5,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:6,
        author:"sribash sarkar",
        imageUrl:"static/images/p4.jpg",
    },
    {
        id:7,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:0,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:1,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:2,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:3,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:4,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:5,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:6,
        author:"sribash sarkar",
        imageUrl:"static/images/p4.jpg",
    },
    {
        id:7,
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
];
 

// const dpimg=[
//         {
//             id:0, 
//             author:"sribash sarkar",
//             imageUrl:"static/images/p3.jpg",
//         },
// ]


const stories =document.querySelector(".stories");
const storiesFullView =document.querySelector(".stories-full-view");
const closeBtn =document.querySelector(".close-btn");
const storyImgFull =document.querySelector(".stories-full-view .story img");
const profileImgFull =document.querySelector(".stories-full-view .profile img");
const storyAuthorFull =document.querySelector(".stories-full-view .story .author");
const nextBtn = document.querySelector(".stories-container .next-btn");
const storiesContent = document.querySelector(".stories-container .content");
const previousBtn = document.querySelector(".stories-container .previous-btn");
const nextBtnFull = document.querySelector(".stories-full-view .next-btn");
const previousBtnFull = document.querySelector(".stories-full-view .previous-btn");
let currentActive =0;

const createStories = () => {
    allStories.forEach((s ,i )=> {
    
        const story = document.createElement("div");
        story.classList.add("story");



        const img = document.createElement("img");
        img.src = s.imageUrl;


        const  author = document.createElement("div");
        author.classList.add("author");
        author.innerHTML = s.author;

        story.appendChild(img);
        story.appendChild(author);
        stories.appendChild(story); 
        story.addEventListener("click",() =>{
            showFullView(i);
        })
    });
};

// const createStories2 = () => {
//     dpimg.forEach((s,j)=>{
//         const profile = document.createElement("div");
//         profile.classList.add("story"); 
//         const img = document.createElement("img");
//         img.src = s.imageUrl;

//         profile.appendChild(img);
//         stories.appendChild(profile); 
//         story.addEventListener("click",() =>{
//             showFullView(j);
//         })
//     })

// }

 createStories();
//  createStories2();
 const showFullView = (index) =>{
    currentActive = index;
    updateFullview();
    storiesFullView.classList.add("actived"); 
    // console.log("hello w")
 };
 closeBtn.addEventListener("click", () => {
    storiesFullView.classList.remove("actived");
 });

 const updateFullview = () =>{
    storyImgFull.src = allStories[currentActive].imageUrl;
    storyAuthorFull.innerHTML = allStories[currentActive].author;
    // profileImgFull.src = allStories[currentActive].imageUrl;

 }

 nextBtn.addEventListener("click",() =>{
    storiesContent.scrollLeft +=300;
 });
 previousBtn.addEventListener("click",() =>{
    storiesContent.scrollLeft -=300;
 });
  
 storiesContent.addEventListener("scroll",()=>{
    if(storiesContent.scrollLeft<= 24){
        previousBtn.classList.remove("actived");
    } else {
        previousBtn.classList.add("actived");
    }
    
    let maxScrollValue = storiesContent.scrollWidth -storiesContent.clientWidth -24;
    
    if(storiesContent.scrollLeft>= maxScrollValue){
        nextBtn.classList.remove("actived");
    } else {
        nextBtn.classList.add("actived");
    }

});

nextBtnFull.addEventListener("click",() =>{
    if(currentActive >=allStories.length -1){
        return;
    }
    currentActive++;
    updateFullview();
})
previousBtnFull.addEventListener("click",() =>{
    if(currentActive <=0){
        return;
    }
    currentActive--;
    updateFullview();
})