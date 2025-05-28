# RebootCommons

A comprehensive web-based survey and analytics platform designed to measure and analyze learning perception and competency changes before and after educational sessions. This application enables learners to evaluate their skills and confidence levels, helping educators assess the effectiveness of their content and improve future educational strategies.

## 🎯 Overview

RebootCommons is a full-stack web application that facilitates:
- Pre/post-lecture assessments for measuring learning outcomes
- User profiling with demographic and lifestyle data
- Advanced data analytics and visualization
- Company-specific and personal survey management
- Real-time dashboard analytics for administrators

## 🏗️ Architecture

### Backend
- **Framework**: Django 5.1.4 with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: JWT tokens with SimpleJWT
- **API**: RESTful API design

### Frontend
- **Framework**: Vue.js 3 with Vite
- **Styling**: Tailwind CSS + PrimeVue components
- **Charts**: Chart.js, ApexCharts for data visualization
- **State Management**: Pinia
- **Routing**: Vue Router

## 🚀 Key Features

### 📊 Survey System
- **Dynamic Survey Creation**: Multiple question types (Rating, Radio, Text, Checkbox)
- **Pre/Post Assessments**: Automatic phase determination
- **Category-based Questions**: Leadership, Entrepreneurship, Positive Psychology Capital
- **Company and Personal Surveys**: Tailored content based on organization

### 👥 User Management
- **Custom User Model** with company associations
- **Demographic Profiling**: Age, gender, education, job position, income
- **Role-based Access**: Regular users vs company administrators
- **JWT Authentication**: Secure token-based authentication

### 📈 Analytics & Visualization
- **Growth Analysis**: Pre/post comparison with percentage improvements
- **Demographic Filtering**: Analysis by age, gender, job role, etc.
- **Interactive Charts**: Bar charts, radar charts, heatmaps
- **Company vs Industry Comparisons**
- **Individual vs Group Performance**

### 🏢 Company Dashboard
- Gender vs Leadership analysis
- Demographic-based performance metrics
- Lifestyle vs Performance correlations
- Real-time statistics and insights

## 📁 Project Structure

```
RebootCommons/
├── backend/                    # Django backend
│   ├── backend/               # Main Django project
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py           # URL routing
│   │   └── wsgi.py           # WSGI configuration
│   ├── account/              # User management app
│   │   ├── models.py         # User and Company models
│   │   ├── api.py            # Authentication APIs
│   │   └── serializer.py     # Data serialization
│   ├── survey/               # Survey management app
│   │   ├── models.py         # Survey, Question, Answer models
│   │   ├── api.py            # Survey APIs and analytics
│   │   └── serializers.py    # Survey data serialization
│   ├── manage.py             # Django management script
│   ├── populate_surveys.py   # Database seeding script
│   └── populate_sample_data.py # Sample data generation
└── wey_frontend/             # Vue.js frontend
    ├── src/
    │   ├── components/       # Reusable Vue components
    │   ├── views/           # Page components
    │   ├── stores/          # Pinia state management
    │   ├── router/          # Vue Router configuration
    │   └── assets/          # Static assets
    ├── public/              # Public assets
    └── package.json         # Frontend dependencies
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.12+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```powershell
   cd backend\backend
   ```

2. **Install Python dependencies**
   ```powershell
   pip install pipenv
   pipenv install
   pipenv shell
   ```

3. **Run database migrations**
   ```powershell
   python manage.py migrate
   ```

4. **Populate database with survey questions**
   ```powershell
   python populate_surveys.py
   ```

5. **Generate sample data (optional)**
   ```powershell
   python populate_sample_data.py
   ```

6. **Create superuser**
   ```powershell
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```powershell
   python manage.py runserver
   ```

The backend will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```powershell
   cd wey_frontend
   ```

2. **Install dependencies**
   ```powershell
   npm install
   ```

3. **Start development server**
   ```powershell
   npm run dev
   ```

The frontend will be available at `http://127.0.0.1:5173`

## 📊 Data Models

### Core Models

#### User & Company
- **User**: Custom user model with company association, demographics
- **Company**: Organizations with course types and descriptions
- **UserExplanation/CompanyExplanation**: Additional context and insights

#### Survey System
- **SurveyType**: Personal vs Corporate surveys
- **CourseType**: Specific programs (Vision House, Leadership & Innovation, Entrepreneurship & Innovation)
- **Question**: Survey questions with categories and types
- **UserSurveyResponse**: User's survey submissions with phase tracking
- **Answer**: Individual question responses

### Question Categories

#### Demographic Questions
- Gender, age, marital status, education level
- Job field, position, employment type, income

#### Lifestyle Questions
- Work-life balance, health habits, stress management
- Learning preferences, technology usage

#### Course-Specific Questions
- **Vision House**: Positive Psychology Capital (Self-efficacy, Optimism, Hope, Resilience)
- **Leadership & Innovation**: Self-leadership, Organizational Commitment
- **Entrepreneurship & Innovation**: Innovation, Proactivity, Risk-taking

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/signup/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Token refresh

### Survey Management
- `GET /api/survey/{survey_type_id}/{course_type_id}/` - Get survey questions
- `POST /api/survey/{survey_type_id}/{course_type_id}/` - Submit survey responses
- `GET /api/survey-types/` - List available survey types
- `GET /api/course-types/{survey_type_id}/` - List courses for survey type

### Analytics
- `GET /api/company/{company_id}/statistics/` - Company statistics
- `GET /api/company/{company_id}/gender-leadership/` - Gender vs leadership analysis
- `GET /api/company/{company_id}/demographic/{type}/` - Demographic analysis
- `GET /api/company/{company_id}/growth-comparison/` - Company vs industry growth
- `GET /api/user/{user_id}/profile/` - User profile and growth data
- `GET /api/user/{user_id}/pre-post-comparison/` - Individual pre/post analysis

## 🎨 Frontend Components

### Key Views
- **SurveyView**: Interactive survey interface with progress tracking
- **Dashboard**: Company analytics and visualizations
- **ProfileView**: Individual user analytics and growth charts
- **CompanyDashboard**: Administrative overview and insights

### UI Components
- **Rating**: Likert scale rating component
- **Question**: Multi-type question component
- **Charts**: Chart.js and ApexCharts integration

## 🔧 Configuration

### Environment Variables
Create `.env` files for environment-specific settings:

#### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOW_ALL_ORIGINS=True
```

#### Frontend (.env)
```
VITE_API_URL=http://127.0.0.1:8000
```

## 🧪 Testing

### Backend Tests
```powershell
cd backend\backend
python manage.py test
```

### Frontend Tests
```powershell
cd wey_frontend
npm run test
```

## 📈 Analytics Features

### Individual Analytics
- Pre/post assessment comparisons
- Category-wise growth analysis
- Personal vs group performance
- Detailed question-level insights

### Company Analytics
- Employee demographics and performance
- Department/role-based analysis
- Industry benchmarking
- Growth trend visualization

### Advanced Features
- Heatmap correlations (lifestyle vs performance)
- Multi-dimensional filtering
- Export capabilities (PDF, Excel)
- Real-time dashboard updates

## 🚀 Deployment

### Production Setup
1. **Database**: Configure PostgreSQL or MySQL
2. **Static Files**: Configure CDN for static assets
3. **Environment**: Set production environment variables
4. **Security**: Configure HTTPS and security headers
5. **Monitoring**: Set up logging and error tracking

### Docker Support (Future Enhancement)
```dockerfile
# Example Dockerfile structure
FROM python:3.12-slim
# Backend setup...

FROM node:16-alpine
# Frontend setup...
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Enhancements

### Planned Features
- **AI-powered Insights**: Machine learning for trend prediction
- **Multi-language Support**: Internationalization
- **LMS Integration**: Canvas, Blackboard connectivity
- **Mobile App**: React Native or Flutter implementation
- **Real-time Collaboration**: WebSocket integration
- **Advanced Reporting**: Custom report builder

### Technical Improvements
- **Multi-tenant Architecture**: Support for multiple organizations
- **Microservices**: Service decomposition for scalability
- **Caching**: Redis integration for performance
- **API Documentation**: Swagger/OpenAPI integration
- **CI/CD Pipeline**: Automated testing and deployment

## 📞 Support

For support and questions:
- **Documentation**: [Project Wiki](link-to-wiki)
- **Issues**: [GitHub Issues](link-to-issues)
- **Email**: support@rebootcommons.com

## 📊 Project Status

- ✅ **Core Features**: Complete
- ✅ **Analytics**: Complete
- ✅ **UI/UX**: Complete
- ⏳ **AI Features**: In Development
- ⏳ **Mobile App**: Planned
- ⏳ **Multi-tenant**: Planned

---

**RebootCommons** - Transforming education through data-driven insights 🚀
