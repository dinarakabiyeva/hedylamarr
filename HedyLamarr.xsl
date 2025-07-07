<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="2.0">
    
    <xsl:output method="html" indent="yes"/>
    
    <xsl:template match="/">
        <html>
            <head>
                <title>
                    <xsl:value-of select="//tei:titleStmt/tei:title"/>
                </title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    h1 {
                        color: #333;
                        border-bottom: 1px solid #ddd;
                    }
                    h2 {
                        color: #444;
                        margin-top: 30px;
                    }
                    .metadata {
                        background-color: #f5f5f5;
                        padding: 15px;
                        border-radius: 5px;
                        margin-bottom: 20px;
                    }
                    .quote {
                        font-style: italic;
                        margin-left: 20px;
                        padding-left: 15px;
                        border-left: 3px solid #ccc;
                    }
                    .note {
                        color: #666;
                        font-size: 0.9em;
                    }
                    .page-break {
                        color: #999;
                        font-style: italic;
                    }
                </style>
            </head>
            <!--Описание метадаты-->
            <body>
                <h1>
                    <xsl:value-of select="//tei:titleStmt/tei:title"/>
                </h1>
                
                <div class="metadata">
                    <p><strong>Author:</strong> 
                        <xsl:value-of select="//tei:titleStmt/tei:author/tei:persName"/>
                    </p>
                    <p><strong>Publisher:</strong> 
                        <xsl:value-of select="//tei:publicationStmt/tei:publisher"/>
                    </p>
                    <p><strong>Publication place:</strong> 
                        <xsl:value-of select="//tei:publicationStmt/tei:pubPlace"/>
                    </p>
                    <p><strong>Publication date:</strong> 
                        <xsl:value-of select="//tei:publicationStmt/tei:pubDate"/>
                    </p>
                    <p><strong>Abstract:</strong> 
                        <xsl:value-of select="//tei:abstract/tei:p"/>
                    </p>
                    <p><strong>Keywords:</strong> 
                        <xsl:for-each select="//tei:keywords/tei:term">
                            <xsl:value-of select="."/>
                            <xsl:if test="position() != last()">, </xsl:if>
                        </xsl:for-each>
                    </p>
                </div>
                
                <h2>About Hedy Lamarr</h2>
                <div class="person-info">
                    <p><strong>Name:</strong> 
                        <xsl:value-of select="//tei:person[@xml:id='HedyLamarr']/tei:persName"/>
                    </p>
                    <p><strong>Birth:</strong> 
                        <xsl:value-of select="//tei:person[@xml:id='HedyLamarr']/tei:birth/@when"/>
                    </p>
                    <p><strong>Death:</strong> 
                        <xsl:value-of select="//tei:person[@xml:id='HedyLamarr']/tei:death/@when"/>
                    </p>
                    <p><strong>Occupations:</strong> 
                        <xsl:for-each select="//tei:person[@xml:id='HedyLamarr']/tei:occupation">
                            <xsl:value-of select="."/>
                            <xsl:if test="position() != last()">, </xsl:if>
                        </xsl:for-each>
                    </p>
                    <p><strong>Note:</strong> 
                        <xsl:value-of select="//tei:person[@xml:id='HedyLamarr']/tei:note"/>
                    </p>
                </div>
                
                 <xsl:apply-templates select="//tei:body/tei:div"/>
            </body>
        </html>
    </xsl:template>

    <!--Сами главы и цитаты-->
     <xsl:template match="tei:div">
        <div class="section">
            <h2>
                <xsl:value-of select="tei:head"/>
            </h2>
            <xsl:apply-templates select="*[not(self::tei:head)]"/>
        </div>
    </xsl:template>
    
    <xsl:template match="tei:note[@type='comment']">
        <p class="note">
            <strong>Comment: </strong><xsl:value-of select="."/>
        </p>
    </xsl:template>
    
    <xsl:template match="tei:quote">
        <blockquote class="quote">
            <xsl:apply-templates/>
        </blockquote>
    </xsl:template>
    
    <xsl:template match="tei:pb">
        <p class="page-break">[Page <xsl:value-of select="substring-after(@facs, 'page')"/>]</p>
    </xsl:template>
    
    <xsl:template match="tei:p">
        <p><xsl:apply-templates/></p>
    </xsl:template>

</xsl:stylesheet>