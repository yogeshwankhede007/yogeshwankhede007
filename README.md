<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yogesh Wankhede - AI-Powered SDET Portfolio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 25%, #2a2a2a 50%, #1a1a1a 75%, #0a0a0a 100%);
            color: #ffffff;
            overflow-x: hidden;
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Navigation */
        .nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(20px);
            z-index: 1000;
            padding: 1rem 0;
            transition: all 0.3s ease;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .nav.scrolled {
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(30px);
            border-bottom: 1px solid rgba(0, 245, 255, 0.3);
        }

        .nav-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, #00f5ff, #ff00f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            color: #ffffff;
            text-decoration: none;
            transition: all 0.3s ease;
            position: relative;
        }

        .nav-links a:hover {
            color: #00f5ff;
        }

        .nav-links a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: linear-gradient(45deg, #00f5ff, #ff00f5);
            transition: width 0.3s ease;
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        /* Hero Section */
        .hero {
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 245, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 0, 245, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(0, 0, 0, 0.8) 0%, transparent 100%);
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        .hero-content {
            z-index: 2;
            position: relative;
        }

        .hero-title {
            font-size: clamp(2rem, 8vw, 4rem);
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #00f5ff, #ff00f5, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient 3s ease-in-out infinite;
        }

        @keyframes gradient {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .hero-subtitle {
            font-size: 1.5rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }

        .hero-description {
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto 2rem;
            opacity: 0.8;
        }

        .cta-button {
            display: inline-block;
            padding: 1rem 2rem;
            background: linear-gradient(45deg, #00f5ff, #ff00f5);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0, 245, 255, 0.3);
        }

        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 245, 255, 0.5);
        }

        /* Animated Background */
        .particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            width: 2px;
            height: 2px;
            background: rgba(255, 255, 255, 0.5);
            animation: particles 20s linear infinite;
        }

        @keyframes particles {
            0% { transform: translateY(100vh) rotate(0deg); }
            100% { transform: translateY(-100vh) rotate(360deg); }
        }

        /* Sections */
        .section {
            padding: 100px 0;
            position: relative;
        }

        .section-title {
            text-align: center;
            font-size: 3rem;
            margin-bottom: 3rem;
            background: linear-gradient(45deg, #00f5ff, #ff00f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* Skills Slider */
        .skills-container {
            position: relative;
            overflow: hidden;
            margin: 2rem 0;
        }

        .skills-slider {
            display: flex;
            transition: transform 0.5s ease;
            gap: 2rem;
        }

        .skill-card {
            min-width: 300px;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .skill-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 245, 255, 0.2);
            border: 1px solid rgba(0, 245, 255, 0.3);
        }

        .skill-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: #00f5ff;
        }

        .skill-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .skill-description {
            opacity: 0.8;
            margin-bottom: 1.5rem;
        }

        .skill-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .skill-tag {
            background: rgba(0, 245, 255, 0.2);
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            border: 1px solid rgba(0, 245, 255, 0.3);
        }

        /* Slider Controls */
        .slider-controls {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }

        .slider-btn {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.5rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .slider-btn:hover {
            background: rgba(0, 245, 255, 0.3);
            transform: scale(1.1);
        }

        /* Expandable Sections */
        .expandable-section {
            margin: 2rem 0;
        }

        .section-header {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(20px);
            padding: 1.5rem;
            border-radius: 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .section-header:hover {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(0, 245, 255, 0.3);
        }

        .section-header h3 {
            font-size: 1.5rem;
            color: #00f5ff;
        }

        .expand-icon {
            font-size: 1.5rem;
            transition: transform 0.3s ease;
        }

        .expand-icon.rotated {
            transform: rotate(180deg);
        }

        .section-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }

        .section-content.expanded {
            max-height: 1000px;
            padding: 2rem;
        }

        /* Certifications Grid */
        .cert-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }

        .cert-card {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            text-align: center;
        }

        .cert-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 245, 255, 0.2);
            border: 1px solid rgba(0, 245, 255, 0.3);
        }

        .cert-icon {
            font-size: 3rem;
            color: #ff00f5;
            margin-bottom: 1rem;
        }

        /* Contact Section */
        .contact-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }

        .contact-card {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .contact-card:hover {
            transform: translateY(-5px);
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(0, 245, 255, 0.3);
        }

        .contact-icon {
            font-size: 3rem;
            color: #00f5ff;
            margin-bottom: 1rem;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.2rem;
            }
            
            .section-title {
                font-size: 2rem;
            }
            
            .skill-card {
                min-width: 250px;
            }
        }

        /* Loading Animation */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 25%, #2a2a2a 50%, #1a1a1a 75%, #0a0a0a 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: opacity 0.5s ease;
        }

        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid #00f5ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .hidden {
            opacity: 0;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <!-- Loading Overlay -->
    <div class="loading-overlay" id="loadingOverlay">
        <div class="loading-spinner"></div>
    </div>

    <!-- Navigation -->
    <nav class="nav" id="navbar">
        <div class="nav-content">
            <div class="logo">YW</div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#skills">Skills</a></li>
                <li><a href="#certifications">Certifications</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero" id="home">
        <div class="particles" id="particles"></div>
        <div class="hero-content">
            <h1 class="hero-title">Yogesh Wankhede</h1>
            <p class="hero-subtitle">Senior SDET | AI-Powered Quality Engineer</p>
            <p class="hero-description">
                Architecting the future of software quality with AI-driven automation frameworks and cutting-edge testing solutions
            </p>
            <a href="https://github.com/yogeshwankhede" target="_blank" class="cta-button">Explore My Work</a>
        </div>
    </section>

    <!-- About Section -->
    <section class="section" id="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div style="text-align: center; max-width: 800px; margin: 0 auto;">
                <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem;">
                    Senior Software Development Engineer in Test (SDET) with extensive experience in architecting and implementing robust automation frameworks. Passionate about delivering high-quality software through innovative testing solutions and AI-powered quality engineering.
                </p>
                <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; color: #00f5ff; margin-bottom: 0.5rem;">🤖</div>
                        <p>AI/ML Testing</p>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; color: #ff00f5; margin-bottom: 0.5rem;">🚀</div>
                        <p>Team Leadership</p>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; color: #00ff88; margin-bottom: 0.5rem;">⚡</div>
                        <p>Full Stack QA</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section class="section" id="skills">
        <div class="container">
            <h2 class="section-title">Technical Arsenal</h2>
            
            <div class="skills-container">
                <div class="skills-slider" id="skillsSlider">
                    <div class="skill-card">
                        <div class="skill-icon">📱</div>
                        <h3 class="skill-title">Mobile Automation</h3>
                        <p class="skill-description">Cross-platform mobile testing expertise with native and hybrid frameworks</p>
                        <div class="skill-tags">
                            <span class="skill-tag">Appium</span>
                            <span class="skill-tag">Espresso</span>
                            <span class="skill-tag">XCUITest</span>
                            <span class="skill-tag">WebdriverIO</span>
                        </div>
                    </div>
                    
                    <div class="skill-card">
                        <div class="skill-icon">🌐</div>
                        <h3 class="skill-title">Web Automation</h3>
                        <p class="skill-description">Modern web testing with cutting-edge frameworks and best practices</p>
                        <div class="skill-tags">
                            <span class="skill-tag">Selenium</span>
                            <span class="skill-tag">Playwright</span>
                            <span class="skill-tag">Cypress</span>
                            <span class="skill-tag">TestNG</span>
                        </div>
                    </div>
                    
                    <div class="skill-card">
                        <div class="skill-icon">⚡</div>
                        <h3 class="skill-title">API & Performance</h3>
                        <p class="skill-description">Comprehensive API testing and performance engineering solutions</p>
                        <div class="skill-tags">
                            <span class="skill-tag">REST Assured</span>
                            <span class="skill-tag">JMeter</span>
                            <span class="skill-tag">Postman</span>
                            <span class="skill-tag">k6</span>
                        </div>
                    </div>
                    
                    <div class="skill-card">
                        <div class="skill-icon">🔄</div>
                        <h3 class="skill-title">DevOps & CI/CD</h3>
                        <p class="skill-description">Automated quality gates and continuous integration expertise</p>
                        <div class="skill-tags">
                            <span class="skill-tag">Jenkins</span>
                            <span class="skill-tag">GitHub Actions</span>
                            <span class="skill-tag">Docker</span>
                            <span class="skill-tag">SonarQube</span>
                        </div>
                    </div>
                    
                    <div class="skill-card">
                        <div class="skill-icon">🤖</div>
                        <h3 class="skill-title">AI/ML Testing</h3>
                        <p class="skill-description">Next-generation testing with AI-powered tools and methodologies</p>
                        <div class="skill-tags">
                            <span class="skill-tag">ChatGPT</span>
                            <span class="skill-tag">GitHub Copilot</span>
                            <span class="skill-tag">TestSigma</span>
                            <span class="skill-tag">Applitools</span>
                        </div>
                    </div>
                </div>
                
                <div class="slider-controls">
                    <button class="slider-btn" onclick="slideSkills('prev')">‹</button>
                    <button class="slider-btn" onclick="slideSkills('next')">›</button>
                </div>
            </div>
            
            <!-- Expandable Sections -->
            <div class="expandable-section">
                <div class="section-header" onclick="toggleSection('programming')">
                    <h3>Programming Languages & Frameworks</h3>
                    <span class="expand-icon">▼</span>
                </div>
                <div class="section-content" id="programming">
                    <div class="cert-grid">
                        <div class="cert-card">
                            <div class="cert-icon">☕</div>
                            <h4>Backend Technologies</h4>
                            <p>Java, Node.js, Python, Spring Boot</p>
                        </div>
                        <div class="cert-card">
                            <div class="cert-icon">🎨</div>
                            <h4>Frontend Technologies</h4>
                            <p>JavaScript, TypeScript, React, Vue.js</p>
                        </div>
                        <div class="cert-card">
                            <div class="cert-icon">🗄️</div>
                            <h4>Database Technologies</h4>
                            <p>MongoDB, PostgreSQL, MySQL, Redis</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="expandable-section">
                <div class="section-header" onclick="toggleSection('cloud')">
                    <h3>Cloud & Monitoring</h3>
                    <span class="expand-icon">▼</span>
                </div>
                <div class="section-content" id="cloud">
                    <div class="cert-grid">
                        <div class="cert-card">
                            <div class="cert-icon">☁️</div>
                            <h4>Cloud Platforms</h4>
                            <p>AWS, Azure, Google Cloud, Firebase</p>
                        </div>
                        <div class="cert-card">
                            <div class="cert-icon">📊</div>
                            <h4>Monitoring & Analytics</h4>
                            <p>DataDog, New Relic, Grafana, Prometheus</p>
                        </div>
                        <div class="cert-card">
                            <div class="cert-icon">🔍</div>
                            <h4>Logging & Tracking</h4>
                            <p>ELK Stack, Splunk, Sentry, CloudWatch</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Certifications Section -->
    <section class="section" id="certifications">
        <div class="container">
            <h2 class="section-title">AI & Modern Testing Certifications</h2>
            <div class="cert-grid">
                <div class="cert-card">
                    <div class="cert-icon">🤖</div>
                    <h4>AI-Powered A/B Testing</h4>
                    <p>SoloLearn - Advanced AI testing methodologies</p>
                </div>
                <div class="cert-card">
                    <div class="cert-icon">💬</div>
                    <h4>ChatGPT Prompt Engineering</h4>
                    <p>For Developers - AI integration in testing</p>
                </div>
                <div class="cert-card">
                    <div class="cert-icon">⚡</div>
                    <h4>Generative AI in Test Automation</h4>
                    <p>Katalon - Pioneering AI-driven testing</p>
                </div>
                <div class="cert-card">
                    <div class="cert-icon">🌱</div>
                    <h4>Enterprise AI Implementation</h4>
                    <p>Syngenta 2024 - AI at enterprise scale</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="section" id="contact">
        <div class="container">
            <h2 class="section-title">Let's Connect</h2>
            <div class="contact-grid">
                <div class="contact-card" onclick="window.open('https://www.linkedin.com/in/ywankhede/', '_blank')">
                    <div class="contact-icon">💼</div>
                    <h4>LinkedIn</h4>
                    <p>Professional Network</p>
                </div>
                <div class="contact-card" onclick="window.open('mailto:yogi.wankhede007@gmail.com', '_blank')">
                    <div class="contact-icon">📧</div>
                    <h4>Email</h4>
                    <p>yogi.wankhede007@gmail.com</p>
                </div>
                <div class="contact-card" onclick="window.open('https://github.com/yogeshwankhede', '_blank')">
                    <div class="contact-icon">💻</div>
                    <h4>GitHub</h4>
                    <p>Code & Projects</p>
                </div>
            </div>
            <div style="text-align: center; margin-top: 3rem;">
                <p style="font-size: 1.5rem; opacity: 0.8;">"Quality is not an act, it is a habit." - Aristotle</p>
            </div>
        </div>
    </section>

    <script>
        // Loading animation
        window.addEventListener('load', function() {
            setTimeout(() => {
                document.getElementById('loadingOverlay').classList.add('hidden');
            }, 1000);
        });

        // Particle animation
        function createParticles() {
            const particles = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
                particles.appendChild(particle);
            }
        }

        // Navbar scroll effect
        window.addEventListener('scroll', function() {
            const navbar = document.getElementById('navbar');
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Skills slider
        let currentSlide = 0;
        const skillsSlider = document.getElementById('skillsSlider');
        const skillCards = document.querySelectorAll('.skill-card');
        const totalSlides = skillCards.length;

        function slideSkills(direction) {
            if (direction === 'next') {
                currentSlide = (currentSlide + 1) % totalSlides;
            } else {
                currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
            }
            
            const slideWidth = skillCards[0].offsetWidth + 32; // card width + gap
            skillsSlider.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
        }

        // Auto-slide skills
        setInterval(() => {
            slideSkills('next');
        }, 5000);

        // Expandable sections
        function toggleSection(sectionId) {
            const content = document.getElementById(sectionId);
            const icon = content.previousElementSibling.querySelector('.expand-icon');
            
            if (content.classList.contains('expanded')) {
                content.classList.remove('expanded');
                icon.classList.remove('rotated');
            } else {
                content.classList.add('expanded');
                icon.classList.add('rotated');
            }
        }

        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Initialize
        createParticles();
        
        // Intersection Observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observe all sections
        document.querySelectorAll('.section').forEach(section => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(50px)';
            section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            observer.observe(section);
        });
    </script>
</body>
</html>
