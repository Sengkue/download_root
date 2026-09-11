<template>
  <ClientOnly>
    <div class="wrapper">
    <div class="sidebar">
      <div class="sidebar-header">
        
        <img src="/about/images/profile.jpg" alt="Image" />
        <div class="lang-switcher" style="margin-top: 15px; text-align: center;">
          <button @click="setLang('en')" :class="['btn btn-sm', currentLang === 'en' ? 'btn-light' : 'btn-outline-light']" style="margin: 0 2px;">EN</button>
          <button @click="setLang('lo')" :class="['btn btn-sm', currentLang === 'lo' ? 'btn-light' : 'btn-outline-light']" style="margin: 0 2px;">LA</button>
          <button @click="setLang('hmn')" :class="['btn btn-sm', currentLang === 'hmn' ? 'btn-light' : 'btn-outline-light']" style="margin: 0 2px;">HMN</button>
        </div>

      </div>
      <div class="sidebar-content">
        <nav class="navbar navbar-expand-md bg-dark navbar-dark">
          <a href="#" class="navbar-brand">Navigation</a>
          <button
            type="button"
            class="navbar-toggler"
            data-toggle="collapse"
            data-target="#navbarCollapse"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="nav navbar-nav">
              <li class="nav-item">
                <a class="nav-link" href="#header"
                  ><span data-i18n="nav_home">Home</span><i class="fa fa-home"></i
                ></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#about"
                  ><span data-i18n="nav_about">About</span><i class="fa fa-address-card"></i
                ></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#skills"
                  ><span data-i18n="nav_skills">Skills</span><i class="fa fa-code"></i
                ></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#experience"
                  ><span data-i18n="nav_experience">Experience</span><i class="fa fa-star"></i
                ></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#service"
                  ><span data-i18n="nav_service">Service</span><i class="fa fa-tasks"></i
                ></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#portfolio"
                  ><span data-i18n="nav_portfolio">Portfolio</span><i class="fa fa-file-archive"></i
                ></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#certificates"
                  ><span data-i18n="nav_certificates">Certificates</span><i class="fa fa-certificate"></i
                ></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#contact"
                  ><span data-i18n="nav_contact">Contact</span><i class="fa fa-envelope"></i
                ></a>
              </li>
              <li class="nav-item" style="margin-top: 30px; border-top: none;">
                <NuxtLink to="/" class="nav-link" style="color: #FF6F61; padding-left: 15px; font-weight: 600;">
                  <i class="fa fa-arrow-left" style="float: none; margin-right: 8px;"></i> <span>Back to Home</span>
                </NuxtLink>
              </li>
            </ul>
          </div>
        </nav>
      </div>
      <div class="sidebar-footer">
        <a href="#"><i class="fab fa-twitter"></i></a>
        <a href="#"><i class="fab fa-facebook-f"></i></a>
        <a href="#"><i class="fab fa-linkedin-in"></i></a>
      </div>
    </div>
    <div class="content">
      <!-- Header Start -->
      <div class="header" id="header">
        <div class="content-inner">
          <p data-i18n="im">I'm</p>
          <h1>Sengvang BM</h1>
          <h2></h2>
          <div class="typed-text">
            Web Designer, Web Developer, Front End Developer, Apps Developer,
            Graphic Designer
          </div>
        </div>
      </div>
      <!-- Header End -->

      <!-- Large Button Start -->
      <div class="large-btn">
        <div class="content-inner">
          <a class="btn" href="resume.pdf"><i class="fa fa-download"></i><span data-i18n="btn_resume">Resume</span></a>
          <a class="btn" href="#"><i class="fa fa-hands-helping"></i><span data-i18n="btn_hire_me">Hire Me</span></a>
        </div>
      </div>
      <!-- Large Button End -->

      <!-- About Start -->
      <div class="about" id="about">
        <div class="content-inner">
          <div class="content-header">
            <h2 data-i18n="header_about">About Me</h2>
          </div>
          <div class="row align-items-center">
            <div class="col-md-6 col-lg-5">
              <img src="/about/images/about.jpg" alt="Image" />
            </div>
            <div class="col-md-6 col-lg-7">
              <p data-i18n="about_text">
                👨‍💻I am a web developer with experience in both frontend and
                backend technologies. I specialize in creating dynamic and
                responsive websites, and I’m passionate about learning new
                tools and techniques to enhance my skills. With strong
                communication abilities, I thrive on collaboration and enjoy
                solving complex challenges in web development.
              </p>
              <a class="btn" href="#" data-i18n="btn_hire_me">Hire Me</a>
            </div>
          </div>
        </div>
      </div>
      <!-- About End -->

      <!-- Skills Start -->
      <div class="skills-section" id="skills">
        <div class="content-inner">
          <div class="content-header">
            <h2 data-i18n="header_skills">Skills</h2>
          </div>
          <div class="row">
            <div class="col-md-6">
              <div class="skills">
                <div class="skill-name">
                  <p>Vue.js</p>
                  <p>45%</p>
                </div>
                <div class="progress">
                  <div class="progress-bar" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 45%"></div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="skills">
                <div class="skill-name">
                  <p>React.js</p>
                  <p>15%</p>
                </div>
                <div class="progress">
                  <div class="progress-bar" role="progressbar" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100" style="width: 15%"></div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="skills">
                <div class="skill-name">
                  <p>Nuxt.js</p>
                  <p>60%</p>
                </div>
                <div class="progress">
                  <div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 60%"></div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="skills">
                <div class="skill-name">
                  <p>Next.js</p>
                  <p>15%</p>
                </div>
                <div class="progress">
                  <div class="progress-bar" role="progressbar" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100" style="width: 15%"></div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="skills">
                <div class="skill-name">
                  <p>Flutter</p>
                  <p>15%</p>
                </div>
                <div class="progress">
                  <div class="progress-bar" role="progressbar" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100" style="width: 15%"></div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="skills">
                <div class="skill-name">
                  <p>Node.js</p>
                  <p>60%</p>
                </div>
                <div class="progress">
                  <div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 60%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Skills End -->

      <!-- Education Start -->
      <div class="education" id="education">
        <div class="content-inner">
          <div class="content-header">
            <h2 data-i18n="header_education">Education</h2>
          </div>
         <div class="row align-items-center">
  <div class="col-md-6">
      <div class="edu-col">
          <span>2007 <i>to</i> 2012</span>
          <h3 data-i18n="edu_primary_title">Primary School</h3>
          <p data-i18n="edu_primary_desc">
              Studied at Thongnamy Primary School.
          </p>
      </div>
  </div>
  <div class="col-md-6">
      <div class="edu-col">
          <span>2012 <i>to</i> 2017</span>
          <h3 data-i18n="edu_secondary_title">Secondary School</h3>
          <p data-i18n="edu_secondary_desc">
              Studied at Thongnamy Secondary School.
          </p>
      </div>
  </div>
  <div class="col-md-6">
      <div class="edu-col">
          <span>2013 <i>to</i> 2019</span>
          <h3 data-i18n="edu_high_title">High School</h3>
          <p data-i18n="edu_high_desc">
              Studied at Viengkham High School.
          </p>
      </div>
  </div>
  <div class="col-md-6">
      <div class="edu-col">
          <span>2019 <i>to</i> 2023</span>
          <h3 data-i18n="edu_bachelor_title">Bachelor in Computer Science (Web Development)</h3>
          <p data-i18n="edu_bachelor_desc">
              National University of Laos, Faculty of Natural Sciences — Department of Computer Science; Major in Web Development.
          </p>
      </div>
  </div>
</div>

        </div>
      </div>
      <!-- Education Start -->

      <!-- Experience Start -->
      <div class="experience" id="experience">
        <div class="content-inner">
          <div class="content-header">
            <h2 data-i18n="header_experience">Experience</h2>
          </div>
          <div class="row align-items-center">
            <div class="col-md-6">
              <div class="exp-col">
                <span data-i18n="exp_sys_date">July 2022 <i>to</i> October 2022</span>
                <h3>Systory Company</h3>
                <h4>—</h4>
                <h5 data-i18n="exp_sys_title">Developer (Frontend &amp; Backend)</h5>
                <p data-i18n="exp_sys_desc">
                  Worked across frontend and backend development.
                </p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="exp-col">
                <span data-i18n="exp_ano_date">November 2023 <i>to</i> January 2024</span>
                <h3>Anousith Express</h3>
                <h4>—</h4>
                <h5 data-i18n="exp_ano_title">Developer (Frontend &amp; Backend)</h5>
                <p data-i18n="exp_ano_desc">
                  Full-stack contributions with emphasis on frontend and backend features.
                </p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="exp-col">
                <span data-i18n="exp_itc_date">2023 <i>to</i> 2024</span>
                <h3>ITCapital (Freelance)</h3>
                <h4>—</h4>
                <h5 data-i18n="exp_itc_title">Freelance Developer (Frontend &amp; Backend)</h5>
                <p data-i18n="exp_itc_desc">
                  Freelance projects covering web frontend and backend.
                </p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="exp-col">
                <span data-i18n="exp_apb_date">2024 <i>to</i> Present</span>
                <h3>APB</h3>
                <h4>—</h4>
                <h5 data-i18n="exp_apb_title">Developer (Frontend &amp; Backend)</h5>
                <p data-i18n="exp_apb_desc">
                  Ongoing full-stack development responsibilities.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Experience Start -->

      <!-- Service Start -->
      <div class="service" id="service">
        <div class="content-inner">
          <div class="content-header">
            <h2 data-i18n="header_service">Service</h2>
          </div>
          <div class="row align-items-center">
            <div class="col-md-6">
              <div class="srv-col">
                <i class="fa fa-desktop"></i>
                <h3 data-i18n="srv_web_title">Web Development</h3>
                <p data-i18n="srv_web_desc">
                  Building dynamic websites and web apps.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Service Start -->

      <!-- Portfolio Start -->
      <div class="portfolio" id="portfolio">
        <div class="content-inner">
          <div class="content-header">
            <h2 data-i18n="header_projects">Projects</h2>
          </div>
          <div class="row">
            <div class="col-lg-12">
              <ul id="portfolio-flters">
                <li data-filter="*" class="filter-active">All</li>
                <li data-filter=".web-dev">Development</li>
              </ul>
            </div>
          </div>
          <div class="row portfolio-container">
            <div class="col-lg-6 col-md-6 portfolio-item web-dev">
              <div class="portfolio-wrap">
                <figure>
                  <img src="/about/images/project/project01.jpg" class="img-fluid" alt="Hongkham Company Group" />
                  <a href="/about/images/project/project01.jpg" class="link-preview" data-lightbox="portfolio" data-title="Hongkham Company Group" title="Preview"><i class="fa fa-eye"></i></a>
                  <a href="#" class="link-details" title="More Details"><i class="fa fa-link"></i></a>
                  <a class="portfolio-title" href="#"
                    >Hongkham Company Group <small style="color: #FF6F61;">(Private)</small> <span>Web Development</span></a
                  >
                </figure>
              </div>
            </div>

            <div class="col-lg-6 col-md-6 portfolio-item web-dev">
              <div class="portfolio-wrap">
                <figure>
                  <img src="/about/images/project/project02.jpg" class="img-fluid" alt="Speed International Transport Lao" />
                  <a href="/about/images/project/project02.jpg" class="link-preview" data-lightbox="portfolio" data-title="Speed International Transport Lao" title="Preview"><i class="fa fa-eye"></i></a>
                  <a href="#" class="link-details" title="More Details"><i class="fa fa-link"></i></a>
                  <a class="portfolio-title" href="#"
                    >Speed International Transport Lao <small style="color: #FF6F61;">(Private)</small> <span>Web Development</span></a
                  >
                </figure>
              </div>
            </div>

            <div class="col-lg-6 col-md-6 portfolio-item web-dev">
              <div class="portfolio-wrap">
                <figure>
                  <img src="/about/images/project/project03.jpg" class="img-fluid" alt="Lao Food" />
                  <a href="/about/images/project/project03.jpg" class="link-preview" data-lightbox="portfolio" data-title="Lao Food" title="Preview"><i class="fa fa-eye"></i></a>
                  <a href="#" class="link-details" title="More Details"><i class="fa fa-link"></i></a>
                  <a class="portfolio-title" href="#"
                    >Lao Food <small style="color: #FF6F61;">(Private)</small> <span>Web Development</span></a
                  >
                </figure>
              </div>
            </div>



            <div class="col-lg-6 col-md-6 portfolio-item web-dev">
              <div class="portfolio-wrap">
                <figure>
                  <img src="/about/images/project/project05.jpg" class="img-fluid" alt="Hmong Shop" />
                  <a href="/about/images/project/project05.jpg" class="link-preview" data-lightbox="portfolio" data-title="Hmong Shop" title="Preview"><i class="fa fa-eye"></i></a>
                  <a href="#" class="link-details" title="More Details"><i class="fa fa-link"></i></a>
                  <a class="portfolio-title" href="#"
                    >Hmong Shop <small style="color: #FF6F61;">(Private)</small> <span>Web Development</span></a
                  >
                </figure>
              </div>
            </div>

            <div class="col-lg-6 col-md-6 portfolio-item web-dev">
              <div class="portfolio-wrap">
                <figure>
                  <img src="/about/images/project/lottery_admin.png" class="img-fluid" alt="Lottery Admin Panel" />
                  <a
                    href="/about/images/project/lottery_admin.png"
                    class="link-preview"
                    data-lightbox="portfolio"
                    data-title="Lottery Admin Panel — Manage operations, open/close times, and winner selection"
                    title="Preview"
                    ><i class="fa fa-eye"></i
                  ></a>
                  <a href="#" class="link-details" title="More Details"
                    ><i class="fa fa-link"></i
                  ></a>
                  <a class="portfolio-title" href="#"
                    >Lottery Admin Panel <span>Web Development</span></a
                  >
                </figure>
              </div>
            </div>

            <div class="col-lg-6 col-md-6 portfolio-item web-dev">
              <div class="portfolio-wrap">
                <figure class="private-projects-card" style="background: #eee; height: 100%; display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px;">
                  <div class="private-card-content">
                    <i class="fa fa-lock" style="font-size: 3rem; color: #999; margin-bottom: 15px;"></i>
                    <h5 style="font-size: 1.1rem; color: #333; margin-bottom: 10px;">Other projects are private and cannot be shown here</h5>
                    <p style="color: #666; font-size: 0.9rem;">Due to confidentiality agreements, further work is hidden.</p>
                  </div>
                </figure>
              </div>
            </div>

          </div>
        </div>
      </div>
      <!-- Portfolio Start -->

      <!-- Certificates Start -->
      <div class="certificates" id="certificates">
        <div class="content-inner">
          <div class="content-header">
            <h2 data-i18n="header_certificates">Certificates</h2>
          </div>
          <div class="row align-items-center">
            <div class="col-md-6 col-lg-4">
              <a href="/about/images/certificate/01.png" data-lightbox="certificates" data-title="Certificate">
                <img src="/about/images/certificate/01.png" alt="Certificate" class="img-fluid certificate-img" />
              </a>
            </div>
          </div>
        </div>
      </div>
      <!-- Certificates End -->

      <!-- Contact Start -->
      <div class="contact" id="contact">
        <div class="content-inner">
          <div class="content-header">
            <h2 data-i18n="header_contact">Contact</h2>
          </div>
          <div class="row align-items-center">
            <div class="col-md-6">
              <div class="contact-info">
                <p><i class="fa fa-user"></i>Sengkuevang BM</p>
                <p><i class="fa fa-tag"></i>Web Designer & Developer</p>
                <p>
                  <i class="fa fa-envelope"></i
                  ><a href="mailto:sengkuevang@gmail.com">sengkuevang@gmail.com</a>
                </p>
                <p>
                  <i class="fa fa-phone"></i
                  ><a href="tel:+8562079929556">+856 207 992 9556</a>
                </p>
                <p>
                  <i class="fa fa-map-marker"></i>13 Street, Vientaine capital, Laos
                </p>
                <div class="social">
                  <a class="btn" href=""><i class="fab fa-twitter"></i></a>
                  <a class="btn" href=""><i class="fab fa-facebook-f"></i></a>
                  <a class="btn" href=""
                    ><i class="fab fa-linkedin-in"></i
                  ></a>
                  <a class="btn" href=""><i class="fab fa-instagram"></i></a>
                  <a class="btn" href=""><i class="fab fa-youtube"></i></a>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form">
                <form>
                  <div class="form-row">
                    <div class="form-group col-md-6">
                      <input
                        type="text"
                        class="form-control"
                        placeholder="Your Name" data-i18n-placeholder="placeholder_name"
                      />
                    </div>
                    <div class="form-group col-md-6">
                      <input
                        type="email"
                        class="form-control"
                        placeholder="Your Email" data-i18n-placeholder="placeholder_email"
                      />
                    </div>
                  </div>
                  <div class="form-group">
                    <input
                      type="text"
                      class="form-control"
                      placeholder="Subject" data-i18n-placeholder="placeholder_subject"
                    />
                  </div>
                  <div class="form-group">
                    <textarea
                      class="form-control"
                      rows="5"
                      placeholder="Message" data-i18n-placeholder="placeholder_message"
                    ></textarea>
                  </div>
                  <div>
                    <button class="btn" type="submit" data-i18n="btn_send">Send Message</button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Contact End -->

      <!-- Footer Start -->
      <div class="footer">
        <div class="content-inner">
          <div class="row align-items-center">
            <div class="col-md-6">
              <p data-i18n="copyright">
                &copy; Copyright by Sengkuevang BM
              </p>
            </div>
            <div class="col-md-6">
              <p>2024/10/25 - <a href="#" data-i18n="privacy">Privacy Policy</a></p>
            </div>
          </div>
        </div>
      </div>
      <!-- Footer Start -->
    </div>
  </div>

  <!-- Back to Top -->
    <a href="#" class="back-to-top"><i class="fa fa-angle-double-up"></i></a>
  </ClientOnly>
</template>

<script setup>
import { onMounted, ref, nextTick } from 'vue';
import { useHead } from '#imports';

definePageMeta({
  layout: 'blank'
});

useHead({
  title: 'Resume sengkuevang',
  link: [
    { href: 'https://fonts.googleapis.com/css2?family=Open+Sans:300;400;600;700;800&display=swap', rel: 'stylesheet' },
    { href: 'https://fonts.googleapis.com/css2?family=Noto+Sans+Lao:wght@300;400;500;600;700&display=swap', rel: 'stylesheet' },
    { href: 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css', rel: 'stylesheet' },
    { href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.0/css/all.min.css', rel: 'stylesheet' },
    { href: '/about/lib/slick/slick.css', rel: 'stylesheet' },
    { href: '/about/lib/slick/slick-theme.css', rel: 'stylesheet' },
    { href: '/about/lib/lightbox/css/lightbox.min.css', rel: 'stylesheet' },
    { href: '/about/css/style.css', rel: 'stylesheet' }
  ],
  script: [
    { src: 'https://code.jquery.com/jquery-3.4.1.min.js', tagPosition: 'bodyClose', defer: true },
    { src: 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js', tagPosition: 'bodyClose', defer: true },
    { src: '/about/lib/easing/easing.min.js', tagPosition: 'bodyClose', defer: true },
    { src: '/about/lib/slick/slick.min.js', tagPosition: 'bodyClose', defer: true },
    { src: '/about/lib/typed/typed.min.js', tagPosition: 'bodyClose', defer: true },
    { src: '/about/lib/waypoints/waypoints.min.js', tagPosition: 'bodyClose', defer: true },
    { src: '/about/lib/isotope/isotope.pkgd.min.js', tagPosition: 'bodyClose', defer: true },
    { src: '/about/lib/lightbox/js/lightbox.min.js', tagPosition: 'bodyClose', defer: true },
    { src: '/about/js/main.js', tagPosition: 'bodyClose', defer: true }
  ],
  bodyAttrs: {
    'data-spy': 'scroll',
    'data-target': '.navbar',
    'data-offset': '51'
  }
});

const currentLang = ref('en');

const translations = {
  en: {
    nav_home: "Home",
    nav_about: "About",
    nav_skills: "Skills",
    nav_experience: "Experience",
    nav_service: "Service",
    nav_portfolio: "Portfolio",
    nav_certificates: "Certificates",
    nav_contact: "Contact",
    im: "I'm",
    btn_resume: "Resume",
    btn_hire_me: "Hire Me",
    header_about: "About Me",
    header_skills: "Skills",
    header_education: "Education",
    header_experience: "Experience",
    header_service: "Service",
    header_projects: "Projects",
    header_certificates: "Certificates",
    header_contact: "Contact",
    about_text: "👨‍💻I am a web developer with experience in both frontend and backend technologies. I specialize in creating dynamic and responsive websites, and I'm passionate about learning new tools and techniques to enhance my skills. With strong communication abilities, I thrive on collaboration and enjoy solving complex challenges in web development.",
    edu_primary_title: "Primary School",
    edu_primary_desc: "Studied at Thongnamy Primary School.",
    edu_secondary_title: "Secondary School",
    edu_secondary_desc: "Studied at Thongnamy Secondary School.",
    edu_high_title: "High School",
    edu_high_desc: "Studied at Viengkham High School.",
    edu_bachelor_title: "Bachelor in Computer Science (Web Development)",
    edu_bachelor_desc: "National University of Laos, Faculty of Natural Sciences — Department of Computer Science; Major in Web Development.",
    exp_sys_date: "July 2022 <i>to</i> October 2022",
    exp_sys_title: "Developer (Frontend & Backend)",
    exp_sys_desc: "Worked across frontend and backend development.",
    exp_ano_date: "November 2023 <i>to</i> January 2024",
    exp_ano_title: "Developer (Frontend & Backend)",
    exp_ano_desc: "Full-stack contributions with emphasis on frontend and backend features.",
    exp_itc_date: "2023 <i>to</i> 2024",
    exp_itc_title: "Freelance Developer (Frontend & Backend)",
    exp_itc_desc: "Freelance projects covering web frontend and backend.",
    exp_apb_date: "2024 <i>to</i> Present",
    exp_apb_title: "Developer (Frontend & Backend)",
    exp_apb_desc: "Ongoing full-stack development responsibilities.",
    srv_web_title: "Web Development",
    srv_web_desc: "Building dynamic websites and web apps.",
    placeholder_name: "Your Name",
    placeholder_email: "Your Email",
    placeholder_subject: "Subject",
    placeholder_message: "Message",
    btn_send: "Send Message",
    copyright: "© Copyright by Sengkuevang BM",
    privacy: "Privacy Policy"
  },
  lo: {
    nav_home: "ໜ້າຫຼັກ",
    nav_about: "ກ່ຽວກັບ",
    nav_skills: "ທັກສະ",
    nav_experience: "ປະສົບການ",
    nav_service: "ບໍລິການ",
    nav_portfolio: "ຜົນງານ",
    nav_certificates: "ໃບຢັ້ງຢືນ",
    nav_contact: "ຕິດຕໍ່",
    im: "ຂ້ອຍແມ່ນ",
    btn_resume: "ຊີວະປະຫວັດ",
    btn_hire_me: "ຈ້າງຂ້ອຍ",
    header_about: "ກ່ຽວກັບຂ້ອຍ",
    header_skills: "ທັກສະ",
    header_education: "ການສຶກສາ",
    header_experience: "ປະສົບການ",
    header_service: "ບໍລິການ",
    header_projects: "ຜົນງານ",
    header_certificates: "ໃບຢັ້ງຢືນ",
    header_contact: "ຕິດຕໍ່",
    about_text: "👨‍💻 ຂ້ອຍແມ່ນນັກພັດທະນາເວັບໄຊ້ທີ່ມີປະສົບການທັງດ້ານ frontend ແລະ backend. ຂ້ອຍຊ່ຽວຊານໃນການສ້າງເວັບໄຊ້ທີ່ຕອບສະໜອງໄດ້ດີ, ແລະມີຄວາມມັກໃນການຮຽນຮູ້ເຄື່ອງມື ແລະ ເຕັກນິກໃໝ່ໆ. ຂ້ອຍມີຄວາມສາມາດໃນການສື່ສານທີ່ດີ, ມັກເຮັດວຽກເປັນທີມ ແລະ ແກ້ໄຂບັນຫາທີ່ຊັບຊ້ອນໃນການພັດທະນາເວັບ.",
    edu_primary_title: "ປະຖົມສຶກສາ",
    edu_primary_desc: "ຮຽນຢູ່ໂຮງຮຽນປະຖົມທົ່ງນາມີ.",
    edu_secondary_title: "ມັດທະຍົມຕົ້ນ",
    edu_secondary_desc: "ຮຽນຢູ່ໂຮງຮຽນມັດທະຍົມຕົ້ນທົ່ງນາມີ.",
    edu_high_title: "ມັດທະຍົມປາຍ",
    edu_high_desc: "ຮຽນຢູ່ໂຮງຮຽນມັດທະຍົມປາຍວຽງຄຳ.",
    edu_bachelor_title: "ປະລິນຍາຕີ ວິທະຍາສາດຄອມພິວເຕີ (ພັດທະນາເວັບ)",
    edu_bachelor_desc: "ມະຫາວິທະຍາໄລແຫ່ງຊາດ, ຄະນະວິທະຍາສາດທຳມະຊາດ — ພາກວິຊາວິທະຍາສາດຄອມພິວເຕີ; ສາຂາການພັດທະນາເວັບ.",
    exp_sys_date: "ກໍລະກົດ 2022 <i>ເຖິງ</i> ຕຸລາ 2022",
    exp_sys_title: "ນັກພັດທະນາ (Frontend & Backend)",
    exp_sys_desc: "ເຮັດວຽກກ່ຽວກັບການພັດທະນາທັງ frontend ແລະ backend.",
    exp_ano_date: "ພະຈິກ 2023 <i>ເຖິງ</i> ມັງກອນ 2024",
    exp_ano_title: "ນັກພັດທະນາ (Frontend & Backend)",
    exp_ano_desc: "ເຮັດວຽກແບບ Full-stack ໂດຍເນັ້ນໃສ່ຄຸນສົມບັດຂອງ frontend ແລະ backend.",
    exp_itc_date: "2023 <i>ເຖິງ</i> 2024",
    exp_itc_title: "ນັກພັດທະນາອິດສະຫຼະ (Frontend & Backend)",
    exp_itc_desc: "ໂຄງການອິດສະຫຼະກວມເອົາທັງ frontend ແລະ backend ຂອງເວັບ.",
    exp_apb_date: "2024 <i>ເຖິງ</i> ປັດຈຸບັນ",
    exp_apb_title: "ນັກພັດທະນາ (Frontend & Backend)",
    exp_apb_desc: "ຮັບຜິດຊອບການພັດທະນາແບບ full-stack ຢ່າງຕໍ່ເນື່ອງ.",
    srv_web_title: "ການພັດທະນາເວັບໄຊ້",
    srv_web_desc: "ສ້າງເວັບໄຊ້ ແລະ ແອັບພລິເຄຊັນເວັບແບບເຄື່ອນໄຫວ.",
    placeholder_name: "ຊື່ຂອງທ່ານ",
    placeholder_email: "ອີເມວຂອງທ່ານ",
    placeholder_subject: "ຫົວຂໍ້",
    placeholder_message: "ຂໍ້ຄວາມ",
    btn_send: "ສົ່ງຂໍ້ຄວາມ",
    copyright: "© ສະຫງວນລິຂະສິດໂດຍ Sengkuevang BM",
    privacy: "ນະໂຍບາຍຄວາມເປັນສ່ວນຕົວ"
  },
  hmn: {
    nav_home: "Tsev",
    nav_about: "Hais Txog",
    nav_skills: "Kev Txawj",
    nav_experience: "Kev Ua Haujlwm",
    nav_service: "Kev Pabcuam",
    nav_portfolio: "Cov Haujlwm",
    nav_certificates: "Daim Ntawv Pov Thawj",
    nav_contact: "Tiv Tauj",
    im: "Kuv yog",
    btn_resume: "Ntawv Qhia Txog Tus Kheej",
    btn_hire_me: "Ntiav Kuv",
    header_about: "Hais Txog Kuv",
    header_skills: "Kev Txawj",
    header_education: "Kev Kawm",
    header_experience: "Kev Ua Haujlwm",
    header_service: "Kev Pabcuam",
    header_projects: "Cov Haujlwm",
    header_certificates: "Daim Ntawv Pov Thawj",
    header_contact: "Tiv Tauj",
    about_text: "👨‍💻 Kuv yog tus tsim web uas muaj kev paub txog frontend thiab backend technologies. Kuv tshwj xeeb hauv kev tsim cov vev xaib uas ua haujlwm zoo thiab teb tau sai. Kuv nyiam kawm cov cuab yeej thiab cov tswv yim tshiab kom txhim kho kuv cov kev txawj. Kuv muaj kev sib txuas lus zoo thiab nyiam koom tes nrog lwm tus los daws cov teeb meem nyuaj hauv web development.",
    edu_primary_title: "Tsev Kawm Qib Qis",
    edu_primary_desc: "Kawm nyob Tsev Kawm Qib Qis Thongnamy.",
    edu_secondary_title: "Tsev Kawm Theem Nrab",
    edu_secondary_desc: "Kawm nyob Tsev Kawm Theem Nrab Thongnamy.",
    edu_high_title: "Tsev Kawm Qib Siab",
    edu_high_desc: "Kawm nyob Tsev Kawm Qib Siab Viengkham.",
    edu_bachelor_title: "Bachelor in Computer Science (Web Development)",
    edu_bachelor_desc: "National University of Laos, Faculty of Natural Sciences — Department of Computer Science; Major in Web Development.",
    exp_sys_date: "Lub 7 hli 2022 <i>txog</i> Lub 10 hli 2022",
    exp_sys_title: "Tus Tsim (Frontend & Backend)",
    exp_sys_desc: "Ua haujlwm txog kev tsim kho frontend thiab backend.",
    exp_ano_date: "Lub 11 hli 2023 <i>txog</i> Lub 1 hli 2024",
    exp_ano_title: "Tus Tsim (Frontend & Backend)",
    exp_ano_desc: "Kev koom tes nrog full-stack uas xyuas txog frontend thiab backend.",
    exp_itc_date: "2023 <i>txog</i> 2024",
    exp_itc_title: "Kev Ntiav Ua Haujlwm Tus Tsim (Frontend & Backend)",
    exp_itc_desc: "Kev ntiav ua haujlwm los xyuas web frontend thiab backend.",
    exp_apb_date: "2024 <i>txog</i> Niaj Hnub No",
    exp_apb_title: "Tus Tsim (Frontend & Backend)",
    exp_apb_desc: "Muaj lub luag haujlwm tas li rau kev tsim kho full-stack.",
    srv_web_title: "Kev Tsim Web",
    srv_web_desc: "Tsim cov websites thiab web apps.",
    placeholder_name: "Koj Lub Npe",
    placeholder_email: "Koj Email",
    placeholder_subject: "Ntsiab Lus",
    placeholder_message: "Lus Qhia",
    btn_send: "Xa Lus",
    copyright: "© Copyright los ntawm Sengkuevang BM",
    privacy: "Kev Cai Tswj Tus Kheej"
  }
};

const setLang = async (lang) => {
  console.log("setLang triggered with:", lang);
  currentLang.value = lang;
  
  await nextTick(); // Wait for Vue to update the DOM with the new button class before manually updating innerHTML
  
  if (typeof document !== 'undefined') {
    document.body.className = document.body.className.replace(/\blang-\S+/g, '');
    document.body.classList.add('lang-' + lang);
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (translations[lang] && translations[lang][key]) {
        el.innerHTML = translations[lang][key];
      }
    });
    
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      if (translations[lang] && translations[lang][key]) {
        el.setAttribute('placeholder', translations[lang][key]);
      }
    });
  }
};

onMounted(() => {
  setTimeout(() => {
    setLang('en');
  }, 100);
});
</script>

<style scoped>
</style>

